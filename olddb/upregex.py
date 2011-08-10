import csv
import re

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

  
  return None
  
  
def family_two(addr):
  #trata de matchear (texto o digit) ( y | esquina ) (texto o digit)
  #((?:\d+\s*(?:bis)?)|(?:\w+[^\s]))\s*(?:[yY]|(?:[eE]sq\.?(?:ina)?))\s*((?:\d+\s*(?:bis)?)|(?:\w+[^\s]))
  
  #trata de matchear (texto o digit ) ( y ) (texto o digit)
  #((?:\d+\s*(?:bis)?)|(?:\w+[^\s]))\s*[yY]\s*((?:\d+\s*(?:bis)?)|(?:\w+[^\s]))
  
  #...anda
  #trata de matchear (digit bis? ) ( y ) (digit bis?)
  #([\w\s\.]+[^\s])\s*[yY]\s*([\w\s\.]+[^\s])
  
  #que hacer con los (digit bis?) y (digit bis?) que tienen altura
  pass
  
def normalizar_superficie(cell, ptr, row):
  re.UNICODE
  
  linea = 'row: '+ str(i) +' input: '+ cell + ', '
  
  m = re.search(ur'(\d+)\s*[xX*]\s*(\d+)', cell)  
  if m is not None:
    linea = linea + 'caso 1 - result:'+ str(int(m.group(1)) * int(m.group(2)))
    if ptr == 0:
      print linea 
    return int(m.group(1)) * int(m.group(2))
  
  m = re.search(ur'(\d+[.,]\d+)', cell)
  if m is not None:
    linea = linea + 'caso 2 - result:'+ m.group(1)
    if ptr == 0:
      print linea 
    return m.group(1)

  m = re.search(ur'(\d+)\sm', cell)
  if m is not None:
    linea = linea + 'caso 3 - result:'+ m.group(1)
    if ptr == 0:
      print linea 
  
    return m.group(1)

  m = re.search(ur',', cell)
  if m is not None:
    linea = linea + 'caso 4 - result: None'
    if ptr == 0:
      print linea 
  
    return None
    
  m = re.search(ur'^\s*(\d+)\s*$', cell)
  if m is not None:
    linea = linea + 'caso 5 - result:'+ m.group(1)
    if ptr == 0:
      print linea 

    return m.group(1)
    
  linea = linea + 'caso None - result: None'
  if ptr == 0:
    print linea 
      
  return None
  

i=0
with open('tbl_Propiedades_temp.csv', 'rb') as fin:
  with open('normalized.csv', 'w') as fout:
    csv.QUOTE_MINIMAL
    csvin   = csv.reader(fin, delimiter=',', quotechar='"')
    
    csvout  = csv.writer(fout, delimiter=',', quotechar='"')
    for row in csvin:
      row[20] = normalizar_superficie(row[20], 0, i)
      #row[21] = normalizar_superficie(row[21], 1)
      #row[22] = normalizar_superficie(row[22], 1)
      csvout.writerow(row)
      #print row[20]
      i=i+1

print 'Done! ' + str(i)
