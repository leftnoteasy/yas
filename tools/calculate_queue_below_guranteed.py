import sys
import math

if __name__ == "__main__":
  folder = sys.argv[1]
  queue = sys.argv[2]
  percent = sys.argv[3]
  totalResource = 100 * 128 * 1024

  guaranteed = totalResource * float(percent)

  allocatedCsv = open(folder + "/" + "counter.queue." + queue + ".allocated.memory.csv")
  pendingCsv = open(folder + "/" + "counter.queue." + queue + ".pending.memory.csv")

  allocated = []
  allocatedCsv.readline()
  for line in allocatedCsv:
    arr = line.split(",")
    if (len(arr) > 1):
      allocated.append(int(arr[1]))

  pending = []
  pendingCsv.readline()
  for line in pendingCsv:
    arr = line.split(",")
    if (len(arr) > 1):
      pending.append(int(arr[1]))

  for i in xrange(0, min(len(allocated), len(pending))):
    if (pending[i] > 0) and (allocated[i] < guaranteed * 0.95):
      print min(guaranteed - allocated[i], pending[i])
    else:
      print 0
