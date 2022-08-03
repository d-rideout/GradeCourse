#!/usr/bin/env python3
'Grade course from gradescope download to prepare submission'

# Assumptions about gradescope:
# * All grades have a single decimal past the decimal point (why???)
# * Assignment columns start at 4 and use 4 columns each

from sys import argv
import decimal as dm
from myAssignments import ass
# Be sure assignment keys are unique across entire course

def ega(ak):
  'explore grade for assignment ak'
  h = {}
  for s in db:
    if ak in db[s]:
      v = db[s][ak]
      if v in h: h[db[s][ak]] += 1 #  print(db[s][k])
      else: h[v] = 1
    else: print('student does not appear on spreadsheet with', ak)
  #   print(h)
  print(h[None], 'Nones')
  del h[None]
  for v,n in sorted(h.items()):
    print(f'{v:4} {n}')
  print('out of', max[ak])

def ckd(vs):
  'check number of decimal places'
  global md
  nd = len(vs.split('.')[1]) # use decimal module method? @ Quick-start Tutorial
  if nd>md:
    print(f'{nd}>{md}:', vs)
    md = nd

    
# Parse command line
if len(argv)<2:
  print('usage: gradeCourse.py <gradescope csv files>')
  print('Be sure that the command line order matches that in myAssignments')
  exit()

db = {} # key SID val dict key: ln fn + those defined in myAssignments
max = {} # keys from myAssignments
ng = [] # num grades per spreadsheet
md = 0  # max decimal places

# Read gradescope grades for main course
print('GradeCourse v0')
dc = dm.getcontext()
# print(dm.getcontext())
dc.traps[dm.Inexact] = True
for fi, fn in enumerate(argv[1:]):
  ng += [0]
  fp = open(fn)
  for ls in fp.readlines():
#     print(ls, end='')
    if ng[fi]:
      ll = ls.split(',')
      k = ll[2]
      if not k in db: db[k] = {}
      db[k]['ln']   = ll[0]
      db[k]['fn']   = ll[1]
      #       for ak, ac in acol[fi].items():
      ac = 4
      for ak in ass[fi]:
        v = ll[ac]
        if v:
          db[k][ak] = dm.Decimal(v)
          ckd(v)
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

ega('hw1')
# print(db)
