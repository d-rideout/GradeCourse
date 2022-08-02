#!/usr/bin/env python3
'Grade course from gradescope download to prepare submission'



from sys import argv
from myAssignments import ass

# Parse command line
if len(argv)<2:
  print('usage: gradeCourse.py <gradescope csv files>')
  print('Be sure that the command line order matches that in myAssignments')
  exit()

db = {} # key SID val dict key: ln fn + those defined in myAssignments
max = {} # keys from myAssignments
ng = [0] # num grades per spreadsheet

# Read gradescope grades for main course
for fi, fn in enumerate(argv[1:]):
  fp = open(fn)
  for ls in fp.readlines():
    print(ls)
    ll = ls.split(',')
  #   print(ll)

    if ng[fi]:
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
        max['hw1'] = float(ll[5])
        max['hw2'] = float(ll[9])
        max['mt1a'] = float(ll[13])
        max['mt1b'] = float(ll[17])
        max['hw3'] = float(ll[21])
        max['hw4'] = float(ll[25])
        max['mt2a'] = float(ll[29])
        max['mt2b'] = float(ll[33])
        max['hw5'] = float(ll[37])
        max['fea'] = float(ll[41])
        max['feb'] = float(ll[45])
  #     else:
  #       if (max['hw1'],max['hw2'],max['mt1a'],) != (): die

    ng[fi] += 1
