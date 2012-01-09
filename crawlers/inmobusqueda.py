import csv
import sys
import re

from urllib2 import Request, urlopen

  
# tiramos la lista de props paginada para una inmo en particular (nos hacemos pasar por chrome)
url = 'http://www.inmobusqueda.com.ar/ficha-73831'

req = Request(url=url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')

# buscamos cosas asi en el html
#<a href="([^\<]*)"><img src="([^\<]*)" border="0"></a>

propid = url[url.rfind('-')+1:]

fichas = filter(lambda x: propid in x, re.findall('<a href="([^\<]*)" border="0">',  urlopen(req).read() ) )

print fichas
