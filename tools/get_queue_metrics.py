import sys
import math

if __name__ == "__main__":
  folder = sys.argv[1]
  queue = sys.argv[2]

  if queue != "cluster":
    metrics = sys.argv[3]
    csv = open(folder + "/" + "counter.queue." + queue + "." + metrics + ".memory.csv")
  else:
    csv = open(folder + "/" + "variable.cluster.allocated.memory.csv")

  data = []
  lineNo = 0
  for line in csv:
    if lineNo == 0:
      lineNo = lineNo + 1
      continue
    arr = line.split(",")
    if (len(arr) > 1):
        print int(arr[1])
