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
from geo.geocell import compute, MAX_GEOCELL_RESOLUTION
from geo.geotypes import Point
from models import Property, PropertyIndex, RealEstate
from search_helper import config_array, alphabet, calculate_price


fout = open('propertybulked.csv', "w")
csvout  = csv.writer(fout, delimiter=',', quotechar='"', lineterminator='\n')

# Atributos del objeto Propiedad para imprimir en el csv del bulker.
attribute_headers = [u'key']

# Itero sobre el metodo 'public_attributes()' de propiedad para obtener los atributos del objeto y generar el csv del bulker.
# Este metodo tambien es utilizado por la librería del 'service/search', pra generar el Json.
for key in  Property.public_attributes():
  attribute_headers.append(u'%s' % unicode(key))

# Agrego atributo realestate (que no es retornado por el método 'public_attributes()') y el string location el cual agrego a mano para generar el csv.
attribute_headers.append(u'realestate')
attribute_headers.append(u'location')
attribute_headers.append(u'location_geocells')
attribute_headers.append(u'status')
 
# Escribo el header de los atributos a bulkear en el csv.
csvout.writerow( map(lambda x: x.encode('utf8'), attribute_headers) )

# Arreglo que contiene los tipos de currency.
currencies = {'US' : 'USD','PE' : 'ARS', '': ''}

csvreader = csv.reader(open('normalized.csv', 'r'), delimiter=',', quotechar='"')
cnames = ["PROP_Id", "PROP_FechaIngreso","PROP_Inmobiliaria","PROP_TIPROP_Id","PROP_PROV_Id","PROP_LOCAL_Id","PROP_PART_Id","PROP_Lugar","PROP_barrio","PROP_Calle","PROP_Nro","PROP_PisoDpto","PROP_DireccionOtros","PROP_ServAgua","PROP_ServLuz","PROP_ServGasNatural","PROP_ServGasGarrafa","PROP_ServCloacas","PROP_ServCable","PROP_ServTelefono","PROP_SupLibre","PROP_SupCubierta","PROP_SupTotal","PROP_Dormitorios","PROP_Plantas","PROP_Ambientes","PROP_Antiguedad","PROP_Banos","PROP_Edificacion","PROP_Amoblado","PROP_Cochera","PROP_Dependencia","PROP_Parque","PROP_VMF","PROP_Patio","PROP_Pileta","PROP_Asfalto","PROP_Terraza","PROP_DescripcionGeneral","PROP_360","PPROP_Mapa","PROP_Vendido","VE_MONEDA","VE_MONTO","AL_MONEDA","AL_MONTO"]
tipoprop = { 'Campo' : 10 , 'Departamento' : 2,'Casa' : 1,'Terreno' : 10 ,'Local' : 5,u'Galpón' : 6,'Chacra' : 10,'Lote' : 10, 'Oficina' : 4,'PH' : 3,u'Fracción' : 10,'Monoambiente' : 2,'Fondos de Comercio' : 5,'Cocheras' : 11 }

#"", "PROP_FechaIngreso","","PROP_TIPROP_Id","","","PROP_PART_Id","PROP_Lugar","","","","","","","","","","","","","","","","","","","","","PROP_Edificacion","","","","","PROP_VMF","","","PROP_Asfalto","","","PROP_360","PPROP_Mapa","PROP_Vendido"

def tryint(val):
  try:
    return int(val)
  except:
    return 0

def tryfloat(val):
  try:
    return float(val)
  except:
    return float(0)
    
    
for inx,row in enumerate(csvreader):

 
  row = map(lambda x: x.decode('utf-8'), row)

  prop = Property()
  
  prop.headline                = '' # db.StringProperty() #no
  prop.main_description        = row[cnames.index("PROP_DescripcionGeneral")] + ' ' + row[cnames.index("PROP_DireccionOtros")] # db.StringProperty() #prop_descripciongeneral
  
  #print type(row[cnames.index("PROP_PROV_Id")])
  
  prop.country                 = u'Argentina' # Argentina
  prop.state                   = row[cnames.index("PROP_PROV_Id")]# PRop_prov_id
  prop.city                    = row[cnames.index("PROP_LOCAL_Id")]# prov local id
  prop.neighborhood            = row[cnames.index("PROP_barrio")]
  prop.street_name             = row[cnames.index("PROP_Calle")] 
  prop.street_number           = int(tryint(row[cnames.index("PROP_Nro")]))
  prop.zip_code                = '' # db.IntegerProperty()
  
  prop.floor                   = row[cnames.index("PROP_PisoDpto")] # db.IntegerProperty()
  prop.building_floors	       = int(row[cnames.index("PROP_Plantas")]) # db.IntegerProperty() #no
    
  prop.images_count            = 0
    
  #prop.user                    = '' # db.ReferenceProperty(User)
  
  # ===================================================== # 
  # Search fields	                                        #
  # ===================================================== #
  
  # AREA FIELDS "PROP_SupLibre","PROP_SupCubierta","PROP_SupTotal"
  prop.area_indoor             = int(tryint(row[cnames.index("PROP_SupCubierta")])) # db.FloatProperty() #cubierta
  prop.area_outdoor            = int(tryint(row[cnames.index("PROP_SupLibre")])) # db.FloatProperty() #
  
  suptotal = int(tryint(row[cnames.index("PROP_SupTotal")]))
  if prop.area_indoor == 0 and prop.area_outdoor == 0 and suptotal != 0:
    prop.area_indoor = suptotal
    
  print str(prop.area_indoor) +' '+ str(prop.area_outdoor) +' '+ str(suptotal)
    
  # ROOMS FIELDS
  prop.rooms	                  = int(tryint(row[cnames.index("PROP_Ambientes")]))  # db.IntegerProperty() @ambientos
  prop.bathrooms               = int(tryint(row[cnames.index("PROP_Banos")]))  # db.IntegerProperty()
  prop.bedrooms                = int(tryint(row[cnames.index("PROP_Dormitorios")]))  # db.IntegerProperty()
  
  # AMENITIES FIELDS GROUP 1
  prop.appurtenance            = int(tryint(row[cnames.index("PROP_Dependencia")])) # db.IntegerProperty()
  prop.balcony                 = 0 # db.IntegerProperty()
  prop.doorman                 = 0 # db.IntegerProperty()
  prop.elevator                = 0 # db.IntegerProperty()
  prop.fireplace               = 0 # db.IntegerProperty()
  prop.furnished               = int(tryint(row[cnames.index("PROP_Amoblado")])) # db.IntegerProperty()
  prop.garage                  = int(tryint(row[cnames.index("PROP_Cochera")])) # db.IntegerProperty()
  
  # AMENITIES FIELDS GROUP 2
  prop.garden                  = int(tryint(row[cnames.index("PROP_Parque")])) # db.IntegerProperty()
  prop.grillroom               = 0 # db.IntegerProperty()
  prop.gym                     = 0 # db.IntegerProperty()
  prop.live_work               = 0 # db.IntegerProperty()
  prop.luxury                  = 0 # db.IntegerProperty()
  prop.pool                    = int(tryint(row[cnames.index("PROP_Pileta")])) # db.IntegerProperty()
  prop.terrace                 = int(tryint(row[cnames.index("PROP_Terraza")])) # db.IntegerProperty()
  
  # AMENITIES FIELDS GROUP 3 & YEAR BUILT
  prop.washer_dryer            = 0 # db.IntegerProperty()
  prop.sum	                   = 0 # db.IntegerProperty()
  
  prop.agua_corriente          = int(tryint(row[cnames.index("PROP_ServAgua")])) # db.IntegerProperty()
  prop.gas_natural             = int(tryint(row[cnames.index("PROP_ServGasNatural")])) #db.IntegerProperty(indexed=False)
  prop.gas_envasado            = int(tryint(row[cnames.index("PROP_ServGasGarrafa")])) #db.IntegerProperty(indexed=False)
  prop.luz                     = int(tryint(row[cnames.index("PROP_ServLuz")])) #db.IntegerProperty(indexed=False)
  prop.cloacas                 = int(tryint(row[cnames.index("PROP_ServCloacas")])) #db.IntegerProperty(indexed=False)
  prop.telefono                = int(tryint(row[cnames.index("PROP_ServTelefono")])) #db.IntegerProperty(indexed=False)
  prop.tv_cable                = int(tryint(row[cnames.index("PROP_ServCable")])) #db.IntegerProperty(indexed=False)
  prop.internet                = 0 #db.IntegerProperty(indexed=False)
  prop.vigilancia              = 0 #db.IntegerProperty(indexed=False)
  prop.monitoreo               = 0 #db.IntegerProperty(indexed=False)
  prop.patio                   = int(tryint(row[cnames.index("PROP_Patio")]))
  
  antiguedad = int(tryint(row[cnames.index("PROP_Antiguedad")]))
  
  #0, 1961, 1991, 2001, 2006, 2011, 9999999999
  if (antiguedad) == 0:
    prop.year_built	             =  0
  elif (antiguedad) < 5:
    prop.year_built	             =  1    
  elif (antiguedad) < 10:
    prop.year_built	             =  5
  elif (antiguedad) < 20:
    prop.year_built	             =  10
  elif (antiguedad) <= 50:
    prop.year_built	             =  50
  else:
    prop.year_built	             =  9999999999
    
    # 1	 # A estrenar
    # 2	 # menor a 5 años
    # 3	 # entre 5 y 10 años
    # 4	 # entre 10 y 20 años
    # 5	 # entre 20 y 50 años
    # 6	 # más de 50 años
  
  # PUBLISHER	
  #prop.realestate              = 3 #int(tryint(row[cnames.index("PROP_Inmobiliaria")])) # db.ReferenceProperty(RealEstate) #prop inmobiliaria
  #prop.realestate              = db.Key.from_path(RealEstate, str(int(tryint(row[cnames.index("PROP_Inmobiliaria")]))), app='viralizar')
  
  # PROPERTY TYPES
  uu = row[cnames.index("PROP_TIPROP_Id")]
  #print uu
  kk = tipoprop[uu]
  
  prop.prop_type_id	                  = alphabet[int(tryint(kk))] # db.StringProperty() crear translate del search helper tipo de propiedad
  #prop.prop_type_id	                  = str(alphabet[4]) # db.StringProperty()
  # PROPERTY STATE & OPERATION & OWNER
  prop.prop_state_id	                = 3 # db.IntegerProperty() #muy bueno
  prop.prop_operation_state_id	      = 1 # db.IntegerProperty() # 1 Disponible
  prop.prop_owner_id	                = 1 # db.IntegerProperty()# 1 inmobiliaria
  prop.prop_operation_id	            = 0
  prop.price_sell                     = 0.0
  prop.price_sell_currency            = currencies['PE']
  prop.price_rent                     = 0.0
  prop.price_rent_currency            = currencies['PE']
  
  #print '---------'
  if tryfloat(row[cnames.index("VE_MONTO")]) != 0.0:
    #print 'soy venta!'
    prop.prop_operation_id	    |= 1
    prop.price_sell              = float(tryfloat(row[cnames.index("VE_MONTO")])) #access op_monto
    prop.price_sell_currency     = currencies[ row[cnames.index("VE_MONEDA")]] #op moneda id

  if tryfloat(row[cnames.index("AL_MONTO")]) != 0.0:
    #print 'soy alquiler!'
    prop.prop_operation_id	|= 2
    prop.price_rent              = float(tryfloat(row[cnames.index("AL_MONTO")]))
    prop.price_rent_currency     = currencies[row[cnames.index("AL_MONEDA")]]
  
  prop.location                = "0,0"
  prop.calculate_inner_values()
  
  #pkey = db.Key.from_path(Property, str(int(tryint(row[cnames.index("PROP_Id")]))))

  arr = []
  
  #KEY
  arr.append( unicode(int(tryint(row[cnames.index("PROP_Id")]))) )
  
  for att in Property.public_attributes():
    val = getattr(prop, att)
    #if att == 'price_rent_computed' or att == 'price_sell_computed':
    #  print u'voy a meter %s = ' + unicode(val)
    arr.append( unicode(val) )
  
  #REALESTATE
  #arr.append( unicode(int(tryint(row[cnames.index("PROP_Inmobiliaria")]))) )
  arr.append( unicode(100) )
  
  #LOCATION
  arr.append( '0.0,0.0' )

  #LOCATION GEOCELLS
  arr.append( repr(prop.location_geocells) )
  
  # STATUS
  if prop.prop_operation_id	== 0:
    arr.append( '2' )
  else:
    arr.append( '1' )
  
  csvout.writerow( map(lambda x: x.encode('utf8'), arr) )
  #if inx > 99:
  print 'Done! metimos las primeras ' + str(inx)
    #break

fout.close()