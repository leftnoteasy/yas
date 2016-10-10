import sys

if __name__ == "__main__":
  line_number = 0
  for line in sys.stdin:
    line_number += 1
    if line.__contains__("assignedContainer queue=root"):
      arr = line.split(" ")
      used = 0
      for s in arr:
        if s.__contains__("absoluteUsedCapacity="):
          used = float(s[len("absoluteUsedCapacity="):])
          break

      if used > 1.001:
        print line_number
        print line
        break
