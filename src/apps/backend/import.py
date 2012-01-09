# -*- coding: utf-8 -*-
"""
    Clases de importacion de diferentes sitios 
      
      * Inmobuesqueda
      * xxxx
      * yyyy
      
    ~~~~~~~~
"""
from __future__ import with_statement

import logging
import re
from urllib2 import Request, urlopen

from google.appengine.ext import db
from google.appengine.api import taskqueue

from webapp2 import cached_property, Response, RequestHandler

class InmoBusqueda(RequestHandler):
  def get(self, **kwargs):
    taskqueue.add(url='/tsko/inmob/list', params={'inmoid':kwargs['inmoid'], 'page':1})
    self.response.write('Bajando de inmobusqueda para id %s' % kwargs['inmoid'])

  def list(self, **kwargs):
    self.request.charset = 'utf-8'
    
    inmoid = self.request.POST['inmoid']
    page   = self.request.POST['page']
    
    # tiramos la lista de props paginada para una inmo en particular (nos hacemos pasar por chrome)
    req = Request(url='http://www.inmobusqueda.com.ar/inmobiliaria.php?pagina=%s&id=%s' % (page, inmoid))
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')

    # buscamos cosas asi en el html
    #<strong><a href="http://www.inmobusqueda.com.ar/ficha-75175">Departamento en Alquiler</a></strong>
    urls = re.findall('<strong><a href="([^\<]*)">',  urlopen(req).read() )
    
    # no hay mas fichas, estamos la ultima pagina+1
    if len(urls) > 0 and urls[0] != '#':
      taskqueue.add(url='/tsko/inmob/list', params={'inmoid':inmoid, 'page':int(page)+1})
    
      # itereamos cada una de las fichas (props)
      for url in urls:
        taskqueue.add(url='/tsko/inmob/prop', params={'url':url})
    else:    
      logging.error('No hay mas')

  def propy(self, **kwargs):
    self.request.charset = 'utf-8'
    url = self.request.POST['url']
    
    # Bajalos la pagina con la ficha
    req = Request(url=url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')
    
    