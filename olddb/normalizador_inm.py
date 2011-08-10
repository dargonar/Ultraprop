# -*- coding: utf-8 -*-
import csv
import re
#import codecs
 

i=0
with open('tbl_PARAM_Inmobiliarias.csv', 'r') as fin:
  with open('normalized_inm.csv', 'w') as fout:
    csvin   = csv.reader(fin, delimiter=',', quotechar='"')
    csvout  = csv.writer(fout, delimiter=',', quotechar='"', lineterminator='\n')
    for row in csvin:
      
      csvout.writerow(row)

      i=i+1

print 'Done! ' + str(i)