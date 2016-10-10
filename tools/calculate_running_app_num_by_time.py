import random
import sys
import os

# read the jobruntime.csv
if __name__ == "__main__":
  f = open(sys.argv[1])

  f.readline()

  maxEnd = -1
  tArr = []
  numApp = []

  for line in f:
    arr = line.split(",")
    if len(arr) == 0:
      continue
    t = (int(arr[len(arr) - 2]), int(arr[len(arr) -1 ]))
    tArr.append(t)
    if t[1] > maxEnd:
      maxEnd = t[1]

  for i in xrange(maxEnd / 1000):
    tot = 0
    for t in tArr:
      if t[0] <= i * 1000 and t[1] >= i * 1000:
        tot = tot + 1

    print tot
