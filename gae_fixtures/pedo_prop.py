# -*- coding: utf-8 -*-
# set PYTHONPATH=%PYTHONPATH%;C:\Program Files (x86)\Google\google_appengine
from __future__ import absolute_import
from datetime import date, datetime , timedelta

import codecs
import random 


from geocell import compute, MAX_GEOCELL_RESOLUTION
from geotypes import Point
from models import Property, PropertyIndex
from search_helper import config_array, alphabet, calculate_price

f = codecs.open('propertybulked.csv', "w", "utf-8")

# Atributos del objeto Propiedad para imprimir en el csv del bulker.
attribute_headers = 'key,'
# Atributos del objeto Propiedad para iterar en la instancia y generar el csv del bulker.
attributes = []

# Itero sobre el metodo 'public_attributes()' de propiedad para obtener los atributos del objeto y generar el csv del bulker.
# Este metodo tambien es utilizado por la librería del 'service/search', pra generar el Json.
for key in  Property.public_attributes():
  attribute_headers += '%s,' % key
  attributes.append(key)

# Agrego atributo realestate (que no es retornado por el método 'public_attributes()') y el string location el cual agrego a mano para generar el csv.
attributes.append('realestate')
attribute_headers += 'realestate,location\r\n'
 
# Escribo el header de los atributos a bulkear en el csv.
f.write(attribute_headers.encode('utf-8'))

# Semilla para las KEY de Property (esta semilla es utilizada por el bulker de imagenes, para tener correspondencia).
seed = 1001

# contadores para mostrar luego los max.
max_geocell_len = 0
max_allcell_len = 0

# Tamaño de la grilla para generar las ubicaciones de las propiedades en el mapa.
gridx = 32
gridy = 32

# Lat y Long que se usa como punto de referencia(caen dentro de CABA) y deltas (dx=dlon, dy=dlat) para generar la cantidad de propiedades 
#  equidistantes a partir de gridx y gridy.
y0 = -34552942/1000000.0
dy = float(-34636033 - -34552942)/1000000.0
dy = float(dy/float(gridy))

x0 = -58357315/1000000.0
dx = float(-58499794 - -58357315)/1000000.0
dx = float(dx/float(gridx))

# Arreglo que contiene los tipos de currency.
currencies = ['USD','ARS']

# Arreglo donde guardo los objetod PropertyIndex correspondiente a cada instancia de Property.
property_indexes = []


for i in range(gridx): 
  for j in range(gridy): 
    prop = Property()
    
    prop.headline                = '' # db.StringProperty()
    prop.main_description        = '_main_description_' # db.StringProperty()
    
    prop.country                 = 'Argentina'
    prop.state                   = 'CABA'
    prop.city                    = 'Buenos Aires'
    prop.neighborhood            = 'Barrio %s' % str(seed) 
    prop.street_name             = 'Calle ' + str(seed)
    prop.street_number           = seed
    prop.zip_code                = str(int(random.randint(1000, 9999))) # db.IntegerProperty()
    
    prop.floor                   = str(random.randint(0, 20)) # db.IntegerProperty()
    prop.building_floors	       = random.randint(0, int(prop.floor)) # db.IntegerProperty()
      
    prop.images_count            = 0
      
    #prop.user                    = '' # db.ReferenceProperty(User)
    
    # ===================================================== # 
    # Search fields	                                        #
    # ===================================================== #
    
    # AREA FIELDS
    prop.area_indoor             = int(random.randrange(30, 400)) # db.FloatProperty()
    prop.area_outdoor            = int(random.randrange(30, 200)) # db.FloatProperty()
    
    # ROOMS FIELDS
    prop.rooms	                 = int(random.randint(1, 10))  # db.IntegerProperty() 
    prop.bathrooms               = int(random.randint(1, 5))  # db.IntegerProperty()
    prop.bedrooms                = int(random.randint(1, 7))  # db.IntegerProperty()
    
    # AMENITIES FIELDS GROUP 1
    prop.appurtenance            = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.balcony                 = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.doorman                 = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.elevator                = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.fireplace               = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.furnished               = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.garage                  = int(random.randint(0, 1)) # db.IntegerProperty()
    
    # AMENITIES FIELDS GROUP 2
    prop.garden                  = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.grillroom               = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.gym                     = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.live_work               = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.luxury                  = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.pool                    = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.terrace                 = int(random.randint(0, 1)) # db.IntegerProperty()
    
    # AMENITIES FIELDS GROUP 3 & YEAR BUILT
    prop.washer_dryer            = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.sum	                   = int(random.randint(0, 1)) # db.IntegerProperty()
    
    prop.agua_corriente          = int(random.randint(0, 1)) # db.IntegerProperty()
    prop.gas_natural             = int(random.randint(0, 1)) #db.IntegerProperty(indexed=False)
    prop.gas_envasado            = int(random.randint(0, 1)) #db.IntegerProperty(indexed=False)
    prop.luz                     = int(random.randint(0, 1)) #db.IntegerProperty(indexed=False)
    prop.cloacas                 = int(random.randint(0, 1)) #db.IntegerProperty(indexed=False)
    prop.telefono                = int(random.randint(0, 1)) #db.IntegerProperty(indexed=False)
    prop.tv_cable                = int(random.randint(0, 1)) #db.IntegerProperty(indexed=False)
    prop.internet                = int(random.randint(0, 1)) #db.IntegerProperty(indexed=False)
    prop.vigilancia              = int(random.randint(0, 1)) #db.IntegerProperty(indexed=False)
    prop.monitoreo               = int(random.randint(0, 1)) #db.IntegerProperty(indexed=False)
    
    prop.year_built	             = int(random.randint(1950, 2011)) # db.IntegerProperty()
    
    # PUBLISHER	
    prop.realestate              = str(int(random.randint(1, 10))) # db.ReferenceProperty(RealEstate)
      
    # PROPERTY TYPES
    prop.prop_type_id	                  = str(alphabet[int(random.randint(1, 11))]) # db.StringProperty()
    #prop.prop_type_id	                  = str(alphabet[4]) # db.StringProperty()
    # PROPERTY STATE & OPERATION & OWNER
    prop.prop_state_id	                = int(random.randint(1, 7)) # db.IntegerProperty()
    prop.prop_operation_state_id	      = int(random.randint(1, 4)) # db.IntegerProperty()
    prop.prop_owner_id	                = int(random.randint(1, 2)) # db.IntegerProperty()
    prop.prop_operation_id	            = int(random.randint(1, 2)) # db.IntegerProperty()
    
    # PRICES FIELDS
    currency                            = currencies[int(random.randint(0, 1))]
    
    prop.price_sell              = float(random.randint(40000, 2000000)) if prop.prop_operation_id == 1 else 0.0
    prop.price_sell_currency     = currency
    prop.price_sell_computed     = calculate_price(prop.price_sell, currency, 'ARS')
    
    prop.price_rent              = float(random.randint(500, 25000)) if prop.prop_operation_id != 1 else 0.0
    prop.price_rent_currency     = currency
    prop.price_rent_computed     = calculate_price(prop.price_rent, currency, 'ARS')
      
    prop.headline = u'%s en %s' % (  config_array['cells']['prop_type_id']['short_descriptions'][alphabet.index(prop.prop_type_id)]
                                  , config_array['multiple_values_properties']['prop_operation_id']['descriptions'][prop.prop_operation_id])
    
    
    
    # geoPT.lat           = y0 + dy*j  #float(random.randrange(-34636033, -34552942)) / 1000000
    # geoPT.latitude      = geoPT.lat
    # geoPT.lon           = x0 + dx*i #float(random.randrange(-58499794, -58357315)) / 1000000
    # geoPT.longitude     = geoPT.lon
    
    point               = Point(y0 + dy*j, x0 + dx*i)
    REQ_location              = '"%f, %f"' % (point.lat, point.lon)
    max_res_geocell, primos   = compute(point, MAX_GEOCELL_RESOLUTION, True)
        
    tmp                       = [max_res_geocell[:res]
                                  for res in
                                    range(1, MAX_GEOCELL_RESOLUTION + 1)]
    
    location_geocells         = sorted(tmp+primos)
    
    if len(location_geocells) > max_geocell_len:
      max_geocell_len  = len(location_geocells)
    
    location_geocells = location_geocells+prop.check_options_ex()
    
    if len(location_geocells) > max_allcell_len:
      max_allcell_len  = len(location_geocells)
      
    soto                      = str(location_geocells) 
    REQ_location_geocells     = soto.replace("['", "[u'").replace(", '", ",u'")
    
    REQ_key                   = str(seed)
    
    prop_str = ''
    for key in attributes:
      val = str(getattr(prop, key))
      if '[' in val and key !='location_geocells' and val != '[]':
        val='"'+val.replace(", '",",u'").replace("['", "[u'")+'"'
      prop_str += val + ','

    prop_str =  REQ_key+','+prop_str+REQ_location+'\r\n'
    
    f.write(prop_str.encode('utf-8'))
    
    property_index = PropertyIndex()
    property_index.key                     = '"%s,%f,%f"' % (REQ_key, point.lat, point.lon)
    property_index.location                = REQ_location
    property_index.location_geocells       = '"'+ REQ_location_geocells +'"'
    property_index.price_sell_computed     = prop.price_sell_computed
    property_index.price_rent_computed     = prop.price_rent_computed
    property_index.price_changed_at        = '2011-0'+str(int(random.randint(1, 7)))+'-04T20:55:54'
    property_index.published_at            = '2010-0'+str(int(random.randint(1, 9)))+'-16T20:55:54' # db.DateTimeProperty()
    property_index.area_indoor             = prop.area_indoor
    property_index.bedrooms                = prop.bedrooms
    property_index.rooms                   = prop.rooms
    property_index.images_count            = prop.images_count
    property_index.realestate              = prop.realestate
    property_index.property                = REQ_key
    
    property_indexes.append(property_index)
    
    seed = seed+1
    
f.close()
print 'max_allcell_len:' + str(max_allcell_len) 
print 'max_geocell_len:' + str(max_geocell_len) 

f = codecs.open('propertyindexbulked.csv', "w", "utf-8")
index_headers = ['key', 'price_sell_computed', 'price_rent_computed', 'price_changed_at', 'published_at'
      , 'area_indoor', 'bedrooms', 'rooms', 'realestate', 'property', 'images_count', 'location', 'location_geocells']
csv_line = ''
for attr in index_headers:
  csv_line += '%s,' % attr
csv_line=csv_line[0:-1]+'\r\n'
f.write(csv_line.encode('utf-8'))

for item in property_indexes:
  csv_line=''
  for attr in index_headers:
    val = str(getattr(item, attr))
    csv_line += val + ','
  csv_line=csv_line[0:-1]+'\r\n'
  f.write(csv_line.encode('utf-8'))
f.close()