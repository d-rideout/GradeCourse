#!/usr/bin/env python3
'Grade course from gradescope download to prepare submission'

from sys import argv
from myAssignments import ass
# Be sure assignment keys are unique across entire course

# Parse command line
if len(argv)<2:
  print('usage: gradeCourse.py <gradescope csv files>')
  print('Be sure that the command line order matches that in myAssignments')
  exit()

db = {} # key SID val dict key: ln fn + those defined in myAssignments
max = {} # keys from myAssignments
ng = [] # num grades per spreadsheet

# Read gradescope grades for main course
for fi, fn in enumerate(argv[1:]):
  ng += [0]
  fp = open(fn)
  for ls in fp.readlines():
#     print(ls, end='')
    if ng[fi]:
      ll = ls.split(',')
      k = ll[2]
      db[k] = {}
      db[k]['ln']   = ll[0]
      db[k]['fn']   = ll[1]
      #       for ak, ac in acol[fi].items():
      ac = 4
      for ak in ass[fi]:
        v = ll[ac]
        if v: db[k][ak] = float(v)
        else: db[k][ak] = None # ?
        ac += 4

      # store maxes
      if ng[fi]==1:
        ac = 5
        for ak in ass[fi]:
          max[ak] = float(ll[ac])
          ac += 4
      else: # check that maxes are constant
        ac = 5
        for ak in ass[fi]:
          if max[ak] != float(ll[ac]):
            print('max mismatch!')
            exit()
          ac += 4

    ng[fi] += 1

print('num grades (plus 1):', ng)
