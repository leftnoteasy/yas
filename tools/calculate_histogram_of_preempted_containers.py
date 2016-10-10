import sys

if __name__ == "__main__":
  f = open(sys.argv[1])

  preempted_containers = set()

  # get preempted containers
  for line in f:
    if line.__contains__("container preempted"):
      arr = line.split(" ")
      for s in arr:
        if s.__contains__("container_"):
          containerId = s.split("=")[1]
          preempted_containers.add(containerId[:len(containerId) - 1])
          break

  f.close()
  f = open(sys.argv[1])

  # memory to number of preempted containers
  memory_to_count = {}
  for line in f:
    if line.__contains__("SchedulerNode: Assigned container"):
      arr = line.split(" ")
      containerId = None
      for s in arr:
        if s.__contains__("container_"):
          containerId = s
          break

      if None != s and preempted_containers.__contains__(containerId):
        if line.find("capacity <memory:") != -1:
          start = line.find("capacity <memory:") + len("capacity <memory:")
          memory = int(line[start : line.find(",", start)])

          if memory_to_count.has_key(memory):
            memory_to_count[memory] = memory_to_count[memory] + 1
          else:
            memory_to_count[memory] = 1

  for i in xrange(1, 33):
    print i * 1024

  print "==========="

  for i in xrange(1, 33):
    if memory_to_count.has_key(i * 1024):
      print memory_to_count[i * 1024]
    else:
      print 0
