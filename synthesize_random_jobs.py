import random
import sys
import os
import math

class Task:
  start = 0
  mem = 0
  type = "map" #map/reduce
  priority = 0
  lifeTime = 0


class Job:
  start = 0
  queue = None
  user = None
  tasks = None

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print 'use "python synthesize_random_jobs.py <output_dir>" to generate SLS load files'
    exit()

  # Define some parameters
  # Resources
  GB = 1024
  minAlloc = 1 * GB
  maxAlloc = 1 * GB

  # Time parameters (in sec)
  MIN = 60
  totalTime = 8 * MIN

  # Queues parameters
  queues = ['a', 'b', 'c', 'd']
  queueCapacities = {'a': 0.05, 'b': 0.1, 'c': 0.25, 'd': 0.60}
  users = ['alice', 'john', 'jack', 'lisa']

  # Nodes parameters
  nNodes = 100
  perNodeMem = 128 * GB
  nodePrefix = "node-"

  # Accumulated resources
  accumulatedResUpperBound = nNodes * perNodeMem * totalTime * 2
  restAccumulatedRes = accumulatedResUpperBound

  # Job accumulated usage
  # Job accumuatedUsage is sigma(task-run-time * task-resource)
  # Job accumuatedUsagePercent obeys numpy.random.exponential distribution
  maxJobAccumulatedUsageRatio = 0.0001
  minJobAccumulatedUsageRatio = 0.000005

  # Task runtime
  minTaskRuntime = totalTime * 0.3
  maxTaskRuntime = totalTime * 0.8

  # Ratio of mapper
  minMapperRatio = 0.7
  maxMapperRatio = 1.0

  # Let's get started
  jobs = []
  while restAccumulatedRes > 0.05 * accumulatedResUpperBound:
    # create next job
    queue = queues[random.randrange(len(queues))]
    user = users[random.randrange(len(users))]

    jobAccumulatedRes = min(restAccumulatedRes, accumulatedResUpperBound \
                            * random.uniform(minJobAccumulatedUsageRatio, maxJobAccumulatedUsageRatio)) \
                            * math.log(100 * queueCapacities[queue])

    job = Job()
    job.queue = queue
    job.user = user
    jobs.append(job)
    job.tasks = []
    #job.start = int(abs(random.gauss((ord(job.queue) - ord('a')) * totalTime / 3.0, 2 * MIN))) * 200

    jobMapperAccumulatedRes = jobAccumulatedRes * random.uniform(minMapperRatio, maxMapperRatio)
    mapperRes = max(minAlloc, int(maxAlloc * random.uniform(0, 1)) / GB * GB)
    jobReducerAccumulatedRes = jobAccumulatedRes - jobMapperAccumulatedRes
    reducerRes = max(minAlloc, int(maxAlloc * random.uniform(0, 1)) / GB * GB)

    # handle mappers
    averageMapperLifetime = random.uniform(minTaskRuntime, maxTaskRuntime)

    print(mapperRes, reducerRes)

    while (jobMapperAccumulatedRes > 0):
      nextRuntime = min(max(minTaskRuntime, random.uniform(averageMapperLifetime * 0.5, averageMapperLifetime * 1.5)), maxTaskRuntime)
      task = Task()
      task.start = 0
      task.type = "map"
      task.priority = 20
      task.lifeTime = nextRuntime
      task.mem = mapperRes
      job.tasks.append(task)
      jobMapperAccumulatedRes = jobMapperAccumulatedRes - mapperRes * nextRuntime
      restAccumulatedRes -= mapperRes * nextRuntime

    # handle reducers
    averageReducerLifetime = random.uniform(minTaskRuntime, maxTaskRuntime)

    while (jobReducerAccumulatedRes > 0):
      nextRuntime = min(max(minTaskRuntime, random.uniform(averageReducerLifetime * 0.5, averageReducerLifetime * 1.5)), maxTaskRuntime)
      task = Task()
      task.start = 0
      task.type = "reduce"
      task.priority = 10
      task.mem = reducerRes
      task.lifeTime = nextRuntime
      job.tasks.append(task)
      jobReducerAccumulatedRes = jobReducerAccumulatedRes - reducerRes * nextRuntime
      restAccumulatedRes -= reducerRes * nextRuntime

  # output
  folder = sys.argv[1]
  try:
    os.makedirs(folder)
  except os.error as e:
    print e

  # output jobs json
  f = open(folder + "/slsjobs.json", 'w')
  s = ''
  for i in range(0, len(jobs)):
    job = jobs[i]
    s += '{'
    s += '"am.type" : "mapreduce",'
    s += '"job.start.ms" : ' + str(job.start) + ','
    s += '"job.end.ms" : 100000000,'
    s += '"job.queue.name" : "' + job.queue + '",'
    s += '"job.user" : "' + job.user + '",'
    s += '"job.id" : "' + 'job_' + str(i) + '",'
    s += '"job.tasks" : ['
    for t in range(0, len(job.tasks)):
      task = job.tasks[t]
      s += '{'
      s += '"container.host" : "/default-rack/' + nodePrefix + str(random.randint(1, nNodes)) + '",'

      s += '"container.priority" : "' + str(task.priority) + '",'
      s += '"container.type" : "' + task.type + '",'
      s += '"container.start.ms" : 0,'
      s += '"container.memory":' + str(task.mem) + ','
      s += '"container.end.ms" : ' + str(long(task.lifeTime * 1000))
      s += '}'
      if t != len(job.tasks) - 1:
        s += ','
    s += '] }'
    if i == len(jobs) - 1:
      s += '\n'
    else:
      s += '\n'

  f.write(s)
  f.close()

  # output nodes json
  f = open(folder + "/slsnodes.json", 'w')
  f.write('{ "rack" : "default-rack", "nodes" : [')

  for i in range(0, nNodes):
    f.write('{ "node" : "' + nodePrefix + str(i) + '"}')
    if i != nNodes - 1:
      f.write(',')

  f.write(']}')

  f.close()





