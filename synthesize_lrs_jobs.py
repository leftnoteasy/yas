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
    print 'use "python synthesize_lrs_jobs.py <output_dir>" to generate SLS load files'
    exit()

  # Define some parameters
  # Resources
  GB = 1024
  minAlloc = 1 * GB
  maxAlloc = 128 * GB

  # Time parameters (in sec)
  MIN = 60

  # Nodes parameters
  nNodes = 100
  perNodeMem = 128 * GB
  nodePrefix = "node-"

  # Let's get started
  jobs = []

  # create 10 jobs in a
  # job has small tasks fulfill the cluster, each of them runs 8 mins
  for i in xrange(10):
    job = Job()
    job.queue = 'a'
    job.user = 'wangda-' + str(i)
    jobs.append(job)
    job.tasks = []
    # we can run (perNodeMem / minAlloc) * nNodes / 10 tasks
    for i in xrange(0, perNodeMem / minAlloc * nNodes / 10):
        task = Task()
        task.start = 0
        task.type = "map"
        task.priority = 20
        task.lifeTime = 8 * MIN
        task.mem = minAlloc * 8
        job.tasks.append(task)

  # create a large job
  # job has large tasks, each of them runs 8 mins
  job = Job()
  job.queue = 'd'
  job.start = 1 * MIN * 500 # job start 60 secs later
  job.user = 'wangda'
  jobs.append(job)
  job.tasks = []
  # run task on 30% of cluster nodes
  for i in xrange(0, 100):
      task = Task()
      task.start = 0
      task.type = "map"
      task.priority = 20
      task.lifeTime = 8 * MIN
      task.mem = minAlloc * 32
      job.tasks.append(task)

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
      s += '"container.host" : "/default/' + nodePrefix + str(random.randint(1, nNodes)) + '",'

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





