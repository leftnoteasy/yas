import ConfigParser
import os
import sys

HADOOP_SOURCECODE_DIR = "hadoop_source_dir"
BRANCH = "branch"
HADOOP_CONF_DIR = "hadoop_conf_dir"
TEST_DATA_DIR = "test_data_dir"
OUTPUT_DIR = "output_dir"
REBUILD = "rebuild"

def read_configs(configPath):
  config = ConfigParser.ConfigParser()
  config.read([configPath])
  return config

def run_test(source_code_dir, branch, conf_dir, test_data_dir, output_dir, rebuild, timeout):
  # Sanity check
  if None == source_code_dir or len(source_code_dir) == 0 or \
    None == branch or len(branch) == 0 or  \
    None == conf_dir or len(conf_dir) == 0 or \
    None == test_data_dir or len(test_data_dir) == 0 or \
    None == output_dir or len(output_dir) == 0 or output_dir == "/":
      exit("Some of the in variable to run test is empty")

  # Setup SLS running environment
  if os.path.isdir(output_dir):
    # make sure we don't do stupid things like remove /
    list = os.listdir(output_dir)
    if len(list) > 3:
      exit("Too many files in output_dir=" + output_dir + ", plz check")
    os.system("rm -rf " + output_dir)
  exit_code = os.system("mkdir -p " + output_dir)
  if 0 != exit_code:
    exit("Failed to create output dir:" + output_dir)

  if rebuild:
    # Build it first
    exit_code = os.system("cd " + source_code_dir + " && git checkout " + branch)
    if 0 != exit_code:
      exit("failed to checkout git branch=" + branch)

    cmd = "cd " + source_code_dir + " && mvn clean install -Pdist -Pyarn-ui -Dtar -DskipTests=true -Dmaven.javadoc.skip=true &> " + output_dir + "/build.out"
    #print ("RUN " + cmd)
    exit_code = os.system(cmd)
    if 0 != exit_code:
      exit("Failed to build Hadoop")

  # Setup environment
  os.putenv('HADOOP_CONF_DIR', conf_dir)
  hadoop_prefix = source_code_dir + "hadoop-dist/target/hadoop-3.0.0-alpha2-SNAPSHOT"
  os.putenv('HADOOP_PREFIX', hadoop_prefix)
  os.putenv('HADOOP_CLIENT_OPTS', "-Xmx16000m -Djava.rmi.server.hostname=172.27.29.0 -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=9993 -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false")

  os.system("echo \"hadoop-conf-dir=$HADOOP_CONF_DIR\"")

  cmd = hadoop_prefix + "/share/hadoop/tools/sls/bin/slsrun.sh  --input-sls=" + test_data_dir + "/slsjobs.json --nodes=" + test_data_dir + \
            "/slsnodes.json --output-dir=" + output_dir + " --print-simulation &>" + output_dir + "/rm.out"
  
  cmd_with_timeout = cmd;

  # runs at most timeout
  if timeout != -1: 
      cmd_with_timeout = "timeout " + str(timeout) + " " + cmd
  print("RUN:" + cmd_with_timeout)
  exit_code = os.system(cmd_with_timeout)
  if 0 != exit_code:
    print("Failed to run sls")

def analysis_output(output_dir, timeout):
  if timeout == -1:
    return

  print("analyzing.." + output_dir + "/rm.out")
  
  f = open(output_dir + "/rm.out")
  lines = 0
  for line in f: 
     if (line.__contains__("ALLOCATED to ACQUIRED")):
         lines = lines + 1
  print("Total has " + str(lines) + " container allocated, " + str(lines / float(timeout)) + " containers allocated per second") 
  f.close()

  f = open(output_dir + "/rm.out")
  accepted = 0
  rejected = 0
  for line in f: 
     if (line.__contains__("Allocation proposal accepted")):
         accepted = accepted + 1
     if (line.__contains__("Failed to accept allocation")):
         rejected = rejected + 1
  print("Total has " + str(accepted) + " proposal accepted, " + str(rejected) + " rejected") 
 

if __name__ == "__main__":
  argc = len(sys.argv)
  path = sys.argv[1]
  timeout = -1;
  if argc > 2:
     timeout = int(sys.argv[2])

  config = read_configs(path)
  for section in config.sections():
    source_code_dir = config.get(section, HADOOP_SOURCECODE_DIR)
    branch = config.get(section, BRANCH)
    conf_dir = config.get(section, HADOOP_CONF_DIR)
    test_data_dir = config.get(section, TEST_DATA_DIR)
    output_dir = config.get(section, OUTPUT_DIR)
    rebuild = config.get(section, REBUILD) == "true"

    print("======================== " + section + " ==============================")
    run_test(source_code_dir, branch, conf_dir, test_data_dir, output_dir, rebuild, timeout)
    analysis_output(output_dir, timeout)
