#!/usr/bin/env python3
'Grade course from gradescope download to prepare submission'

# Assumptions about gradescope:
# * All grades have a single decimal past the decimal point (why???)
# * Assignment columns start at 4 and use 4 columns each

from sys import argv
import decimal as dm
from myAssignments import *
# Be sure assignment keys are unique across entire course

def grade(s, a):
  if a in db[s]:
    g = db[s][a]
    if g: return g
    else: return 0
  else:
    print('no', a, 'grade for', s)
    return 0

def sg(s):
  "compute a student's numerical grade"

  print('\n', s, end=' ')

  # HW 1
  g = grade(s, 'hw1')
  if g: hw1 = dm.Decimal(g/mga['hw1'])
  else: hw1 = 0
#   print(s, hw1, mga['hw1'], end=' | ')
  
  # HW 2-5
  hwt = ('hw2', 'hw3', 'hw4', 'hw5')
  hw25 = []
  for hwa in hwt:
    g = grade(s, hwa)
    if g: hw25.append(g/mga[hwa])
    else: hw25.append(0)
#     print(g, mga[hwa], end='  ')
  hw25g = dm.Decimal((sum(hw25)-min(hw25))/3)
  print(f'HW: f25={hw25g} hw1={hw1} {hw25}') # min(hw25))

  # MT1
  mt = [grade(s, 'mt1a')/mga['mt1a'], grade(s, 'mt1b')/mga['mt1b']]
#   if grade(s, 'mt1a')!=None and grade(s, 'mt1b')!=None:
#     print('um')
#     exit()
  mtg = max(mt)
  print('midterm:', max(mt))

  # Final
  fe = [grade(s, 'fea')/mga['fea'], grade(s, 'feb')/mga['feb']]
  feg = max(fe)
  print('final:', max(fe))

  # MATLAB HW
  mlt = ('ml1', 'ml2', 'ml3', 'ml4', 'ml5')
  mlhw = []
  for mla in mlt:
    mlhw.append(grade(s, mla)/mga[mla])
  mlhwg = sum(sorted(mlhw)[2:])/3
  print('MATLAB HW:', mlhwg, sorted(mlhw)[2:]) # , sorted(mlhw))

  # MATLAB Quiz
  mlq = dm.Decimal(grade(s, 'mlfq')/mga['mlfq'])
  print('MATLAB Q:', mlq)

  print('hw:', dm.Decimal(.3)*(hw1 + 3*hw25g)/4, dm.Decimal(.3)*hw25g)
  hwg = max(dm.Decimal(.3)*(hw1 + 3*hw25g)/4, dm.Decimal(.3)*hw25g)
  
#   ghw1 = dm.Decimal(.3)*(hw1 + 3*hw25g)/4
#   + dm.Decimal(.3)*mtg
#   + dm.Decimal(.3)*feg
#   + dm.Decimal(.06)*mlhwg
#   + dm.Decimal(.04)*dm.Decimal(mlq)
#   g = dm.Decimal(.3)*hw25g + dm.Decimal(.3)*mtg + dm.Decimal(.3)*feg + dm.Decimal(.06)*mlhwg + dm.Decimal(.04)*mlq
  g = hwg + dm.Decimal(.3)*mtg + dm.Decimal(.3)*feg + dm.Decimal(.06)*mlhwg + dm.Decimal(.04)*mlq
  print('final grade=', g)

def ega(ak):
  'explore grade for assignment ak'
  print(f'\nExploring grades for assignment {ak}:')
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
  print('out of', mga[ak])

def ckd(vs):
  'check number of decimal places'
  global md
  nd = len(vs.split('.')[1]) # use decimal module method? @ Quick-start Tutorial
  if nd>md:
    print(f'{nd}>{md}:', vs, end='  ')
    md = nd
    return True
  return False

def epair(ak1, ak2):
  'explore pair of assignments'
  for s in db:
    if ak1 in db[s] and ak2 in db[s] and db[s][ak1] and db[s][ak2]: print(s, db[s][ak1], db[s][ak2])


# Parse command line
if len(argv)<2:
  print('usage: gradeCourse.py <gradescope csv files>')
  print('Be sure that the command line order matches that in myAssignments')
  exit()

db = {} # key SID val dict key: ln fn + those defined in myAssignments
mga = amax # keys from myAssignments
ng = [] # num grades per spreadsheet
md = 0  # max decimal places

# Read gradescope grades for main course
print('GradeCourse v0')
dc = dm.getcontext()
# print(dm.getcontext())
# dc.traps[dm.Inexact] = True
dc.prec = 9
for fi, fn in enumerate(argv[1:]):
  print('parsing', fn)
  ng += [0]
#   if isinstance(ass[fi], list):
#     ng += [0]
#     spec = False # special file requiring specific column specification
#   else:
#     ng += [-1] # skip maxes line for now
#     spec = True
  fp = open(fn)
  for ls in fp.readlines():
#     print(ls, end='')
    if ng[fi] >= nskip[fi]:
      ll = ls.split(',')
      if debug: print(ll)
      if nskip[fi]==1: k = ll[2] # student id
      else: k = ll[3] # student id HACK
      if debug: print(f'key=[{k}]')
      if not k: continue # skip Student, Test with no SID
      if not k in db: db[k] = {}
      if nskip[fi]==1: # HACK! actually this should not be needed
        # , splits last and first names in canvas file too
        db[k]['ln']   = ll[0]
        db[k]['fn']   = ll[1]
      #       for ak, ac in acol[fi].items():
      ac = 4
      for ak in ass[fi]:
        if ak in spcol: ac = spcol[ak] # special columns
        v = ll[ac]
        if v:
          if debug: print(f'ak=[{ak}] ac=[{ac}] v=[{v}]')
          db[k][ak] = dm.Decimal(v)
          if ckd(v): print('from', k)
        else: db[k][ak] = None # ?
        ac += 4

      # store maxes
      if nskip[fi]==1: # HACK
        if ng[fi]==1:
          ac = 5
          for ak in ass[fi]:
            mga[ak] = dm.Decimal(ll[ac])
            ac += 4
        else: # check that maxes are constant
          ac = 5
          for ak in ass[fi]:
            if mga[ak] != dm.Decimal(ll[ac]):
              print('max mismatch!')
              exit()
            ac += 4

    ng[fi] += 1

print('num grades (plus 1):', ng, '\n')

assignments = ass[0]+ass[1]+ass[2]
# for a in ass[0]+ass[1]+ass[2]:
#   ega(a)

# epair('mt1a', 'mt1b')
# epair('mt2a', 'mt2b')
# epair('fea', 'feb')
# no one took both exams

# print(assignments)
for s in db: sg(s)
