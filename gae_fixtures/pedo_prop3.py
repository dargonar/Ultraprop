# -*- coding: utf-8 -*-
# set PYTHONPATH=%PYTHONPATH%;C:\Program Files (x86)\Google\google_appengine
from __future__ import absolute_import
from datetime import date, datetime , timedelta

import inspect,os,sys
mydir = os.path.dirname( inspect.currentframe().f_code.co_filename )
gpath = r'c:\Archivos de programa'
sys.path[0:0] = [r'%s\Google\google_appengine\lib\django'%gpath, \
                 r'%s\Google\google_appengine\lib\yaml\lib'%gpath, \
                 r'%s\Google\google_appengine'%gpath,\
                mydir+r'\..\src\lib', mydir+r'\..\src\distlib']
print sys.path

import codecs
import random 
import csv
import sys

from google.appengine.ext import db
from models import Property, PropertyIndex, RealEstate
from search_helper import config_array, alphabet, calculate_price


fout = open('realstatebulked.csv', "w")
csvout  = csv.writer(fout, delimiter=',', quotechar='"', lineterminator='\n')

# Atributos del objeto Propiedad para imprimir en el csv del bulker.
attribute_headers = [u'key']

# Itero sobre el metodo 'public_attributes()' de propiedad para obtener los atributos del objeto y generar el csv del bulker.
# Este metodo tambien es utilizado por la librería del 'service/search', pra generar el Json.
for key in  RealEstate.public_attributes():
  attribute_headers.append(u'%s' % unicode(key))

# Agrego atributo realestate (que no es retornado por el método 'public_attributes()') y el string location el cual agrego a mano para generar el csv.
#attribute_headers.append(u'realestate')
#attribute_headers.append(u'location')
 
# Escribo el header de los atributos a bulkear en el csv.
csvout.writerow( map(lambda x: x.encode('utf8'), attribute_headers) )

# Arreglo que contiene los tipos de currency.
currencies = {'US' : 'USD','PE' : 'ARS', '': ''}

csvreader = csv.reader(open('normalized_inm.csv', 'r'), delimiter=',', quotechar='"')
cnames = ["INM_Id","INM_Nombre","INM_Direccion","INM_Telefono","INM_Fax","INM_Email","INM_Url","INM_Pass","INM_Destacados","INM_Desabilitada","INM_Color"]
#"","","","","","","","INM_Pass","INM_Destacados","INM_Desabilitada","INM_Color"


def tryint(val):
  try:
    return int(val)
  except:
    return 0

def tryfloat(val):
  try:
    return float(val)
  except:
    return 0
    
    
for row in csvreader:

  row = map(lambda x: x.decode('utf-8'), row)

  
  # logo                = blobstore.BlobReferenceProperty()
  # name                = db.StringProperty()
  # website             = db.LinkProperty(indexed=False)
  # email               = db.EmailProperty(indexed=False)
  
  # title               = db.StringProperty()
  # fax_number          = db.StringProperty(indexed=False)
  # telephone_number    = db.StringProperty(indexed=False)
  # telephone_number2   = db.StringProperty(indexed=False)
  
  # address             = db.StringProperty(indexed=False)
  # zip_code            = db.StringProperty()
  # updated_at          = db.DateTimeProperty(auto_now=True)
  # created_at          = db.DateTimeProperty(auto_now_add=True)
  
  # enable              = db.IntegerProperty()
  
  arr = []
  
  #KEY
  
  arr.append( str(int(tryint(row[cnames.index("INM_Id")])))) 
  arr.append( '' )
  arr.append( row[cnames.index("INM_Nombre")]) 
  arr.append( row[cnames.index("INM_Url")] )
  arr.append( row[cnames.index("INM_Email")] )
  arr.append( '' )
  arr.append( row[cnames.index("INM_Fax")] )
  arr.append( row[cnames.index("INM_Telefono")] )
  arr.append( '' )
  arr.append( row[cnames.index("INM_Direccion")] )
  arr.append( '' )
  arr.append( '1' )
  
  
  csvout.writerow( map(lambda x: x.encode('utf8'), arr) )

fout.close()