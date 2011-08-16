# -*- coding: utf-8 -*-
import logging

from datetime import datetime
from models import Property
from re import *
from backend_forms import status_choices
from search_helper import config_array, alphabet

def do_headlinify(prop):
    
    descs = config_array['multiple_values_properties']['prop_operation_id']['descriptions']
    
    # Ponemos el headline
    ops = []
    for i in range(0,len(descs)):
      if i & prop.prop_operation_id:
        ops.append(descs[i])
        
    return u'%s en %s' % ( config_array['cells']['prop_type_id']['short_descriptions'][alphabet.index(prop.prop_type_id)]
                                  , '/'.join(ops))
  
def do_descriptify(prop, cols, small=False):
  items = { 'rooms'        : { 'desc': 'ambiente'   ,'small':'amb.'       ,'plural': True  },
            'bedrooms'     : { 'desc': 'dormitorio' ,'small':'dorm.'      ,'plural': True  },
            'bathrooms'    : { 'desc': u'baño'      ,'small':u'bano.'     ,'plural': True  },
            'area_indoor'  : { 'desc': u'm² cub.'   ,'small':u'm² cub.'   ,'plural': False },
            'area_outdoor' : { 'desc': u'm² descub.','small':u'm² descub.','plural': False }, }
            
  parts = []
  for col in cols:
    # Tenemos esta columna?
    if col not in items:
      continue

    item = items[col]      
    
    # Tomamos el valor, como son todos integers si es 0(=sin dato) no lo mostramos
    val = int(getattr(prop, col))
    if not val:
      continue
    
    # Ponemos la descripción y pluralizamos si hay que hacerlo y si no es small (el small no se pluraliza)
    desc = item['desc']
    if not small:    
      if item['plural'] and val > 1:
        desc += 's'
    elif 'small' in item:
      desc = item['small']

    # Agregamos al arreglo
    parts.append( u'%d %s' % (val, desc) )
  
  return ', '.join(parts)

def do_addressify(prop):

  parts = []
  
  street = prop.street_name
  tmp = street.lower()
  if ' entre ' not in tmp and ' y ' not in tmp:
    if prop.street_number > 0:
      street += ' al ' + str(int(int(prop.street_number/100)*100))

  parts.append(street)
  
  if prop.neighborhood and prop.neighborhood.strip() != '':
    parts.append( prop.neighborhood.strip() )

  parts.append(prop.hack_city)
  return ', '.join(parts)


def do_statusfy(val):
  for choice in status_choices:
    if choice[0] == val:
      return choice[1]
  
  return ''
  
def do_time_distance_in_words(from_date, since_date = None, target_tz=None, include_seconds=False):
  '''
  Returns the age as a string
  '''
  if since_date is None:
    since_date = datetime.now(target_tz)

  distance_in_time = since_date - from_date
  distance_in_seconds = int(round(abs(distance_in_time.days * 86400 + distance_in_time.seconds)))
  distance_in_minutes = int(round(distance_in_seconds/60))

  if distance_in_minutes <= 1:
    if include_seconds:
      for remainder in [5, 10, 20]:
        if distance_in_seconds < remainder:
          return "menos de %s seconds" % remainder
      if distance_in_seconds < 40:
        return "medio minuto"
      elif distance_in_seconds < 60:
        return "menos de un minuto"
      else:
        return "1 minuto"
    else:
      if distance_in_minutes == 0:
        return "menos de un minuto"
      else:
        return "1 minuto"
  elif distance_in_minutes < 45:
    return "%s minutos" % distance_in_minutes
  elif distance_in_minutes < 90:
    return "cerca de 1 hora"
  elif distance_in_minutes < 1440:
    return "cerca de %d hora" % (round(distance_in_minutes / 60.0))
  elif distance_in_minutes < 2880:
    return "1 d&iacute;a"
  elif distance_in_minutes < 43220:
    return "%d dias" % (round(distance_in_minutes / 1440))
  elif distance_in_minutes < 86400:
    return "cerca de 1 mes"
  elif distance_in_minutes < 525600:
    return "%d meses" % (round(distance_in_minutes / 43200))
  elif distance_in_minutes < 1051200:
    return "cerca de 1 a&ntilde;o"
  else:
    return "mas de %d a&ntilde;os" % (round(distance_in_minutes / 525600))

def do_currencyfy(number, small=False, **args):
  temp = "%.1f" % number
  # if small:
    # temp = "%d" % int(number)
  temp = temp.replace('.', ',')
  profile = compile(r"(\d)(\d\d\d[.,])")
  while 1:
      temp, count = subn(profile,r"\1.\2",temp)
      if not count: break
  if small:
    if ',' in temp:
      return temp[:-2]
  return temp
  
def do_pricefy(property, operation_type = None, small=False, **args):
  number = property.price_rent
  cur = property.price_rent_currency
  if (operation_type is None and property.price_sell_computed>0.0) or int(operation_type) == Property._OPER_SELL:
    number = property.price_sell
    cur = property.price_sell_currency
  return '<small>'+cur+'</small>'+do_currencyfy(number, small=small)
  