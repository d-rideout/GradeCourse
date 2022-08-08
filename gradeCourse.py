#!/usr/bin/env python3
'Grade course from gradescope+canvas download to egrades submission'

# Assumptions about gradescope:
# * All grades have a single decimal past the decimal point (why??)
# * Assignment columns start at 4 and use 4 columns each

from sys import argv
import csv
import decimal as dm # deprecate?
# import fractions as fm
# Put all content specific to your course into a myAssignments.py module:
from myAssignments import *
# Be sure assignment keys are unique across entire course

def asscol(x):
  'returns sequence of assignment, col pairs'
  if isinstance(x, dict):
    for a,c in x.items(): yield a,c
  elif isinstance(x, list):
    col = 4
    for a in x:
      yield a, col
      col += 4

def tsg(s):
  'trace student grade'
  # This should not be necessary -- it is already provided by sg below.
  print(f"{s} {db[s]['ln']} {db[s]['fn']}:")
  print(f"HW: hw1 = {grade(s, 'hw1')}/{mxga['hw1']} =", grade(s, 'hw1')/mxga['hw1'])
  hwt = ('hw2', 'hw3', 'hw4', 'hw5')
  hw25 = []
  for hwa in hwt:
    g = grade(s, hwa)
    if g: hw25.append(f"{g}/{mxga[hwa]}")
    else: hw25.append(0)
#   hw25g = dm.Decimal((sum(hw25)-min(hw25))/3)
#   print(f'    f25={hw25g} {hw25}')
  print(f'    hw25={hw25}')

  print(f"MT1 {grade(s, 'mt1a')}/{mxga['mt1a']} {grade(s, 'mt1b')}/{mxga['mt1b']}")
  print(f"MT2 {grade(s, 'mt2a')}/{mxga['mt2a']} {grade(s, 'mt2b')}/{mxga['mt2b']}")

  print(f"FE {grade(s, 'fea')}/{mxga['fea']} {grade(s, 'feb')}/{mxga['feb']}")

  print(f"MATLAB HW", end='')
  for a in ('ml1', 'ml2', 'ml3', 'ml4', 'ml5'):
    print(f" {grade(s, a)}/{mxga[a]}")


def clg(g):
  'compute letter grade'
  if g>=.97: return 'A+'
  elif g>=.93: return 'A'
  elif g>=.90: return 'A-'
  elif g>=.87: return 'B+'
  elif g>=.83: return 'B'
  elif g>=.80: return 'B-'
  elif g>=.77: return 'C+'
  elif g>=.73: return 'C'
  elif g>=.70: return 'C-'
  else: return 'F'
  
def grade(s, a):
  if a in db[s]:
    g = db[s][a]
    if g: return g
    else: return 0
  else:
    print('no', a, 'grade for', s)
    return 0


def sg(s):
  "compute student (SID s)'s grade"

#   print('\n', s, end=' ')
# a 'request' may appear before in output before this is called
  print(f"{s} {db[s]['fn']} {db[s]['ln']}:") #, end=' ')

  # HW 1
  g = grade(s, 'hw1')
  if g: hw1 = dm.Decimal(g/mxga['hw1'])
  else: hw1 = 0
#   print(s, hw1, mxga['hw1'], end=' | ')
  
  # HW 2-5
  hwt = ('hw2', 'hw3', 'hw4', 'hw5')
  hw25 = []
  for hwa in hwt:
    g = grade(s, hwa)
    if g: hw25.append(g/mxga[hwa])
    else: hw25.append(0)
#     print(g, mxga[hwa], end='  ')
  hw25g = dm.Decimal((sum(hw25)-min(hw25))/3)
  print(f'HW: hw1={hw1} f25={hw25g} {hw25}') # min(hw25))

  # MT
  mt1 = [grade(s, 'mt1a')/mxga['mt1a'], grade(s, 'mt1b')/mxga['mt1b']]
#   if grade(s, 'mt1a')!=None and grade(s, 'mt1b')!=None:
#     print('um')
#     exit()
  mt2 = [grade(s, 'mt2a')/mxga['mt2a'], grade(s, 'mt2b')/mxga['mt2b']]
  if mt2[1]: mt2[1] += 7/mxga['mt2b']
  # I should not have done this, as I did not even give a max threshold!!
  mtg = max(mt1+mt2)
  print('midterm:', mtg)

  # Final
  fe = [grade(s, 'fea')/mxga['fea'], grade(s, 'feb')/mxga['feb']]
  feg = max(fe)
  print('final:', max(fe))

  # MATLAB HW
  mlt = ('ml1', 'ml2', 'ml3', 'ml4', 'ml5')
  mlhw = []
  for mla in mlt:
    mlhw.append(grade(s, mla)/mxga[mla])
  mlhwg = sum(sorted(mlhw)[2:])/3
  print('MATLAB HW:', mlhwg, sorted(mlhw)[2:]) # , sorted(mlhw))

  # MATLAB Quiz
  mlq = dm.Decimal(grade(s, 'mlfq')/mxga['mlfq'])
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
  lg = clg(g)
  print('final grade=', g, clg(g), '\n')
  db[s]['lg'] = lg
  if lg in gradeDist: gradeDist[lg] += 1
  else: gradeDist[lg] = 1
  return lg

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
  print('out of', mxga[ak])

def ckdf(vs):
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

# ------------------------------------------------------------------------------
# Parse command line
if len(argv)<2:
  print('usage: gradeCourse.py <grade csv files> [-cl class list files]')
  print('Be sure that the command line order matches that in myAssignments')
  exit()

db = {} # key SID val dict key: ln fn sec lg + those defined in myAssignments
mxga = amax # (max grade for assignment) keys from myAssignments
ng = [] # num grades per spreadsheet
md = 0  # max decimal places
gradeDist = {}
cll = [] # class list list
clm = False # class list mode

# Read grades for main course
# ---------------------------
print('GradeCourse v0')
# dc = dm.getcontext()
# # print(dm.getcontext())
# # dc.traps[dm.Inexact] = True
# dc.prec = 9
for fi, fn in enumerate(argv[1:]):
  print('parsing', fn)
  if fn=='-cl':
    clm = True
    continue
  elif clm:
    cll.append(fn)
    continue
  ng += [0] # add num grades count for this spreadsheet

#   if isinstance(ass[fi], list):
#     ng += [0]
#     spec = False # special file requiring specific column specification
#   else:
#     ng += [-1] # skip maxes line for now
#     spec = True
  fp = open(fn)
#   for ls in fp.readlines():
  for ll in csv.reader(fp):
    if ng[fi] >= nskip[fi]: # skip header lines
      if debug: print(ll)

      # Read SID & names
#       if nskip[fi]==1: k = ll[2] # student id
#       else: k = ll[3] # student id HACK
      k = ll[sidc[fi]]
      if debug: print(f'key=[{k}]')
      if not k: continue # skip Student, Test with no SID
      if not k in db: db[k] = {}
#       if nskip[fi]==1: # HACK! actually this should not be needed
        # , splits last and first names in canvas file too
      # Assume first occurrence of name for this SID is correct
      if not 'ln' in db[k]:
        db[k]['ln']   = ll[lnc]
        if fnc!=None: db[k]['fn']   = ll[fnc]
      #       for ak, ac in acol[fi].items():

      # Read grades
      #       ac = 4
      #       for ak in ass[fi]:
      #         if ak in spcol: ac = spcol[ak] # special columns
      for ak, ac in asscol(ass[fi]):
        v = ll[ac]
        if v:
          if debug: print(f'ak=[{ak}] ac=[{ac}] v=[{v}]')
          db[k][ak] = dm.Decimal(v)
#           db[k][ak] = fm.Fraction(v) # dm.Decimal(v)
          if ckdf(v): print('from', k)
        else: db[k][ak] = None # ?
#         ac += 4

        # store maxes
        #       if nskip[fi]==1: # HACK
        if ak in amax: continue # skip if max is specified in myAssignments.py module
        if ng[fi]==nskip[fi]: # @ first line of data
#           ac = 5
#           for ak in ass[fi]:
          mxga[ak] = dm.Decimal(ll[ac+1])
#             ac += 4
        else: # check that maxes are constant
          ac = 5
          for ak in ass[fi]:
            if mxga[ak] != dm.Decimal(ll[ac]):
              print('max mismatch!')
              exit()
            ac += 4

    ng[fi] += 1

print(f'num grades (plus {nskip}):', ng, '\n')

# assignments = ass[0]+ass[1]+ass[2]
# for a in ass[0]+ass[1]+ass[2]:
#   ega(a)

# epair('mt1a', 'mt1b')
# epair('mt2a', 'mt2b')
# epair('fea', 'feb')
# no one took both exams

# print(assignments)
# for s in db: sg(s)

# Read section assignments
if len(cll)>1:
  print("Unsure how to handle multiple class lists at the moment")
  exit()
elif len(cll):
  fp = open(cll[0])
  # secs = {}
  ofp = {} # key sec val fp
  for ls in fp.readlines():
    ll = ls.split('\t')
    if ll[0]=='Last Name': continue
    print('request from class list file:', ll) # 'request for grade'
    sid = ll[2]
    sec = ll[4]
    db[sid]['sec'] = sec
  #   if not sec in secs: secs[sec] = 1
  #   secs[sec] += 1

    lg = sg(sid)
    if sec in ofp:
  #     print('\t',join((db[sid]['ln'])), file=ofp[sec])
      print('\t'.join((ll[0],ll[1],ll[2],sec,lg)), file=ofp[sec])
    else:
      ofp[sec] = open(sec+'.tsv', 'w')
      print('\t'.join(('Last Name', 'First Name', 'Student ID', 'SectionId', 'Final_Assigned_Egrade')), file=ofp[sec])
      print('\t'.join((ll[0],ll[1],ll[2],sec,lg)), file=ofp[sec])

print()
# print(sorted(secs))

for g in sorted(gradeDist): print(g, gradeDist[g])
