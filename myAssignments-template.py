# ass is list of
# * lists for gradescope spreadsheets
# * dicts for spreadsheets from other sources (such as canvas)
#   dict val is col num corresponding to assignment in spreadsheet
ass = ['hw1 hw2 mt1a mt1b hw3 hw4 mt2a mt2b hw5 fea feb'.split(),
       'ml1 ml2 ml3 ml4 ml5'.split(),
       {'mlfq':6}]

sidc = (2,2,3) # sid col

lnc, fnc = 0,1 # columns which hold last and first names in first spreadsheet
# Use None for fnc if there is only one name column in the first spreadsheet?

# number of header cols to skip for each spreadsheet
nskip = (1,1,2)

# Max grades for non-gradescope assignments
amax = {'mlfq':6}

debug = False
