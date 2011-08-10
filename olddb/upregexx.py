import csv
import re

def family_one(addr):
  re.UNICODE
  m = re.search(ur'(\d+\s*(?:bis)?)\s*\(\s*(\d+\s*(?:bis)?)\s*[yY]\s*(\d+\s*(?:bis)?)\)', addr)
  if m is not None:
    return m

  m = re.search(ur'(\d+\s*(?:bis)?)\s*[-eE]\s*/?(?:NTRE|ntre)?\s*(\d+\s*(?:bis)?)\s*[yY]\s*(\d+\s*(?:bis)?)', addr)
  #m = re.search(ur'(\d+\s*(?:bis)?\w+?)\s*[-eE]\s*/?(?:NTRE|ntre)?\s*(\d+\s*(?:bis)?)\s*[yY]\s*(\d+\s*(?:bis)?\w?)', addr)
  if m is not None:
    return m

  #m = re.search(ur'(\d+)\s(\d+)\s[yY]\s(\d+)', addr)
  m = re.search(ur'(\d+\s*(?:bis)?)\s(\d+\s*(?:bis)?)\s*[yY]\s*(\d+\s*(?:bis)?)', addr)
  if m is not None:
    return m

  m = re.search(ur'([a-zA-z\u00E1\u00E9\u00ED\u00F3\u00FA\u00F1\s\.]+)\s+[-eE]\s*/?(?:NTRE|ntre)?\s*([a-zA-z\u00E1\u00E9\u00ED\u00F3\u00FA\u00F1\s\.]+)\s*[yY]\s*([a-zA-z\u00E1\u00E9\u00ED\u00F3\u00FA\u00F1\s\.]+)', addr)
  if m is not None:
    return m

    
  #family2
    
  m = re.search(ur'^([a-zA-z\u00E1\u00E9\u00ED\u00F3\u00FA\u00F1\s\.]+)\s*[yY]\s*([a-zA-z\u00E1\u00E9\u00ED\u00F3\u00FA\u00F1\s\.]+)$', addr)
  if m is not None:
    return m
    
  m = re.search(ur'^([a-zA-z\u00E1\u00E9\u00ED\u00F3\u00FA\u00F1\s\.]+)\s*[yY]\s*([a-zA-z\u00E1\u00E9\u00ED\u00F3\u00FA\u00F1\s\.]+)$', addr)
  if m is not None:
    return m    
    
  m = re.search(ur'^(\d+\s*(?:bis)?)\s*[yY]\s*(\d+\s*(?:bis)?)$', addr)
  if m is not None:
    return m
    
  m = re.search(ur'(\d+\s*(?:bis)?)\s[eE]sq\.?(?:uina)?\s(\d+\s*(?:bis)?)', addr)
  if m is not None:
    return m
  
  m = re.search(ur'([a-zA-z\u00E1\u00E9\u00ED\u00F3\u00FA\u00F1\s\.]+)\s[eE]sq\.?(?:uina)?\s([a-zA-z\u00E1\u00E9\u00ED\u00F3\u00FA\u00F1\s\.]+)', addr)
  if m is not None:
    return m
  
  m = re.search(ur'^([a-zA-z\u00E1\u00E9\u00ED\u00F3\u00FA\u00F1\s\.]+)$', addr)
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
  #(\d+\s*(?:bis)?)\s*[yY]\s*(\d+\s*(?:bis)?)
  
  #que hacer con los (digit bis?) y (digit bis?) que tienen altura
  
  pass

i=0
with open('temp.csv', 'rb') as fin:
  with open('match.csv', 'w') as fout2:
    with open('nonmatch.csv', 'w') as fout:
      csvout  = csv.writer(fout, delimiter=',', quotechar='"')
      csvout2 = csv.writer(fout2, delimiter=',', quotechar='"')
      csvread = csv.reader(fin, delimiter=',', quotechar='"')
      for row in csvread:
        m = family_one(row[9])
        if m is None:
          csvout.writerow([ row[9] ])
          i=i+1
        else:
          csvout2.writerow([ row[9] ] + list(m.groups()))
 
print 'Done! ' + str(i)
