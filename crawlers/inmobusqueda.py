import csv
import sys
import re

from urllib2 import Request, urlopen

# ID de la inmobiliaria
inmo = int(sys.argv[1])
page = 1

#fout = open('props.csv', "w")
#csvout = csv.writer(fout, delimiter=',', quotechar='"', lineterminator='\n')

has_more_pages = True

while has_more_pages and page < 2:
  
  # tiramos la lista de props paginada para una inmo en particular (nos hacemos pasar por chrome)
  req = Request(url='http://www.inmobusqueda.com.ar/inmobiliaria.php?pagina=%d&id=%d' % (page, inmo))
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')

  # buscamos cosas asi en el html
  #<strong><a href="http://www.inmobusqueda.com.ar/ficha-75175">Departamento en Alquiler</a></strong>
  fichas = re.findall('<strong><a href="([^\<]*)">',  urlopen(req).read() )
  
  # no hay mas fichas, estamos la ultima pagina+1
  if len(fichas) == 0 or (len(fichas) == 1 and fichas[0] == '#'):
    has_more_pages = False
    continue
    
  # iteramos las fichas
  for ficha in fichas:
    ficha
    
  print fichas
  page = page + 1
