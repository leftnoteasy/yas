# Introduction
This project is used to run Scheduler Load Simulator on different environment / configs
# Usage
## Setup configuration file

Example of configuration file see below
```
[original CS]
hadoop_source_dir=/Users/wtan/sandbox/hadoop/
branch=without-lock-improvement
hadoop_conf_dir=/Users/wtan/project/github/yarn_application_synthesizer/configs/hadoop-conf-cs/
test_data_dir=/tmp/sls-data
output_dir=/tmp/sls-out

[improved CS]
hadoop_source_dir=/Users/wtan/sandbox/hadoop/
branch=lock-improvement
hadoop_conf_dir=/Users/wtan/project/github/yarn_application_synthesizer/configs/hadoop-conf-cs/
test_data_dir=/tmp/sls-data
output_dir=/tmp/sls-out
```

Each section is an individual test, each test has following required attributes, all pathes need to be absolute path:
- `hadoop_source_dir`: where is the Hadoop source code folder, test framework will build/package Hadoop for each section
- `branch`: which **local** Hadoop branch you want to run the test
- `hadoop_conf_dir`: path to hadoop configuration directory
- `test_data_dir`: path to SLS test data, it expects `slsjobs.json`  `slsnodes.json` inside the directory
- `output_dir`: where to store output files, test program will cleanup and create it for you if not existed, but you should have write permission on that path

## Run it

Update `scheduler-load-test.cfg` correctly and
Call `python test-framwork/run-tests.py configs/scheduler-load-test.cfg` to run the test.

Output looks like:
```
======================== original CS ==============================
Already on 'without-lock-improvement'
RUN cd /Users/wtan/sandbox/hadoop/ && mvn clean install -Pdist -Pyarn-ui -Dtar -DskipTests=true -Dmaven.javadoc.skip=true &> /tmp/sls-out/build.out
hadoop-conf-dir=/Users/wtan/project/github/yarn_application_synthesizer/configs/hadoop-conf-cs/
RUN:time /Users/wtan/sandbox/hadoop/hadoop-dist/target/hadoop-3.0.0-alpha2-SNAPSHOT/share/hadoop/tools/sls/bin/slsrun.sh  --input-sls=/tmp/sls-data/slsjobs.json --nodes=/tmp/sls-data/slsnodes.json --output-dir=/tmp/sls-out --print-simulation &>/tmp/sls-out/rm.out

real    8m51.774s
user    8m41.998s
sys    1m28.158s
======================== improved CS ==============================
Switched to branch 'lock-improvement'
RUN cd /Users/wtan/sandbox/hadoop/ && mvn clean install -Pdist -Pyarn-ui -Dtar -DskipTests=true -Dmaven.javadoc.skip=true &> /tmp/sls-out/build.out
hadoop-conf-dir=/Users/wtan/project/github/yarn_application_synthesizer/configs/hadoop-conf-cs/
RUN:time /Users/wtan/sandbox/hadoop/hadoop-dist/target/hadoop-3.0.0-alpha2-SNAPSHOT/share/hadoop/tools/sls/bin/slsrun.sh  --input-sls=/tmp/sls-data/slsjobs.json --nodes=/tmp/sls-data/slsnodes.json --output-dir=/tmp/sls-out --print-simulation &>/tmp/sls-out/rm.out

real    8m48.426s
user    8m31.398s
sys    1m29.861s
```

# Examples
- Example data please refer to: `data/`
- Example configs please refer to `config/`
- There're some script inside this repo to generate simulated workload, but code quality of them is too crappy, so ignore them.

# TODO
- Now it assumes code is in Hadoop trunk, and version is `3.0.0-alpha2`, should be fixed.

