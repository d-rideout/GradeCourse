#!/usr/bin/env python3
'Grade course from gradescope download to prepare submission'

from sys import argv
from myAssignments import acol

# Parse command line
if len(argv)<2:
  print('usage: gradeCourse.py <gradescope csv files>')
  print('Be sure that the command line order matches that in myAssignments')
  exit()

db = {} # key SID val dict key: ln fn sid + those defined in myAssignments
max = {} # keys from myAssignments
ng = [0]

# Read gradescope grades for main course
fp = open(fn)
for ls in fp.readlines():
  print(ls)
  ll = ls.split(',')
#   print(ll)

  if ng:
    k = ll[2]
    db[k] = {}
    db[k]['ln']   = ll[0]
    db[k]['fn']   = ll[1]
    db[k]['hw1']  = float(ll[4])
    db[k]['hw2']  = float(ll[8])
    db[k]['mt1a'] = float(ll[12])
    db[k]['mt1b'] = float(ll[16])
    db[k]['hw3']  = float(ll[20])
    db[k]['hw4']  = float(ll[24])
    db[k]['mt2a'] = float(ll[28])
    db[k]['mt2b'] = float(ll[32])
    db[k]['hw5']  = float(ll[36])
    db[k]['fea']  = float(ll[40])
    db[k]['feb']  = float(ll[44])

    # store maxes
    if ng==1:
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
      
  ng += 1
