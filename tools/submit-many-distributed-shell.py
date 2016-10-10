import subprocess

def runProcess(jarFile, numContainer):
    cmd = 'hadoop jar ' + jarFile + ' -jar ' + jarFile + ' -shell_command pwd -num_containers=' + numContainer + \
          ' -master_memory=400 -container_memory=400'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while(True):
      retcode = p.poll() #returns None while subprocess is running
      line = p.stdout.readline()
      if line.__contains__("ACCEPTED") or line.__contains__("RUNNING"):
        print "SUBMIT one app, with #container=" + numContainer
        break
      if(retcode is not None):
        break

if __name__ == "__main__":
