# -*- coding: utf-8 -*-
from google.appengine.ext import db
from google.appengine.ext.blobstore import BlobInfo
#import google.appengine.api.datastore.Entity

def create_foreign_key(kind, key_is_id=True):
  def generate_foreign_key_lambda(value):
    if value is None:
      return None

    # if key_is_id:
      # value = int(value)
    #print ' generate_foreign_key_lambda:' + kind +' |value:' + value
    value = int(value)
    return db.Key.from_path(kind, str(value))

  return generate_foreign_key_lambda
  
def get_float(kind):
  def toto(value):
    if value is None:
      return 0.0
    return float(value)
  return toto
  
def get_geo(kind):
  def tete(value):
    if value is None:
      return db.GeoPt(lat=0.0, lon=0.0)
    lat, lng = value.split(',')
    return db.GeoPt(lat=float(lat), lon=float(lng))
  return tete
  
def get_blob_key(kind):
  def titi(value):
    return  BlobInfo.get(str(value)).key() #blobstore.get(str(value))
  return titi

def post_get_blob_key(input_dict, entity_instance, bulkload_state):
  entity_instance['file'] = BlobInfo.get(str(entity_instance['file'])).key()
  return entity_instance