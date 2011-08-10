# -*- coding: utf-8 -*-
import csv
import re
import codecs

def family_one(addr):
  re.UNICODE
  m = re.search(ur'(?u)([\w\s\.]+[^\s])\s*\(\s*([\w\s\.]+[^\s])\s*[yY]\s*([\w\s\.]+[^\s])\)', addr)
  if m is not None:
    return m

  m = re.search(ur'(?u)([\w\s\.]+[^\s])\s*[-eE]\s*/?(?:NTRE|ntre)?\s*([\w\s\.]+[^\s])\s*[yY]\s*([\w\s\.]+[^\s])', addr)
  #m = re.search(ur'(?u)(\d+\s*(?:bis)?\w+?)\s*[-eE]\s*/?(?:NTRE|ntre)?\s*([\w\s\.]+[^\s])\s*[yY]\s*(\d+\s*(?:bis)?\w?)', addr)
  if m is not None:
    return m

  #m = re.search(ur'(?u)(\d+)\s(\d+)\s[yY]\s(\d+)', addr)
  m = re.search(ur'(?u)([\w\s\.]+[^\s])\s([\w\s\.]+[^\s])\s*[yY]\s*([\w\s\.]+[^\s])', addr)
  if m is not None:
    return m
    
  #family2
    
  m = re.search(ur'(?u)^([\w\s\.]+[^\s])\s*[yY]\s*([\w\s\.]+[^\s])$', addr)
  if m is not None:
    return m
  
    
  m = re.search(ur'(?u)([\w\s\.]+[^\s])\s[eE]sq\.?(?:uina)?\s([\w\s\.]+[^\s])', addr)
  if m is not None:
    return m
  
  
  m = re.search(ur'(?u)^([\w\s\.]+[^\s])$', addr)
  if m is not None:
    return m
    
  return u'0'
  
 
def normalizar_superficie(cell):
  re.UNICODE
 
  m = re.search(ur'(\d+)\s*[xX*]\s*(\d+)', cell)  
  if m is not None:
    return unicode(int(m.group(1)) * int(m.group(2)))
  
  m = re.search(ur'(\d+[.,]\d+)', cell)
  if m is not None:
    return unicode(int(float(m.group(1).replace(',','.'))))

  m = re.search(ur'(\d+)\s?[mM]', cell)
  if m is not None:
    return m.group(1)
    
  m = re.search(ur'^\s*(\d+)\s*$', cell)
  if m is not None:
    return m.group(1)
    
  return u''
  

i=0
with open('tbl_propiedades_temp.csv', 'r') as fin:
  with open('normalized.csv', 'w') as fout:
    csvin   = csv.reader(fin, delimiter=',', quotechar='"')
    csvout  = csv.writer(fout, delimiter=',', quotechar='"', lineterminator='\n')
    for row in csvin:

      #lleva a unicode
      row = map(lambda x: x.decode('utf-8'), row)

      row[20] = normalizar_superficie(row[20])
      row[21] = normalizar_superficie(row[21])
      row[22] = normalizar_superficie(row[22])

      print row
      #print '===>' + hex(row[-1][)
      
      #vuelve a utf8
      row = map(lambda x: x.encode('utf-8'), row)
      
      csvout.writerow(row)

      i=i+1

print 'Done! ' + str(i)