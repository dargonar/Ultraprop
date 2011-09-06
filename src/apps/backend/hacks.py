# -*- coding: utf-8 -*-
"""
    hacks handlers
    ~~~~~~~~
"""

import logging

from utils import need_auth, BackendHandler 

class VerArchivo(BackendHandler):
  @need_auth(roles='ultraadmin', code=505)
  def get(self, **kwargs):
    return self.render_response(kwargs['archivo'].replace('-','/'))

class IndexRedir(BackendHandler):
  def get(self, **kwargs):
    return self.redirect_to('frontend/home')
    
# Redireccion por si alguien entra con url vieja
class OldRealEstateRedirect(BackendHandler):
  def get(self, **kwargs):
    realestate = self.request.GET['INM_Id']
    self.redirect_to('realestate/search', realestate=realestate)

# -----------------------------Mappers para 1.2 --------------------
from google.appengine.api.images import get_serving_url
from google.appengine.ext import deferred
from taskqueue import Mapper
from models import Property, ImageFile, RealEstate, Plan
from myfilters import do_slugify

class ImageFixMapper(Mapper):
  KIND    = ImageFile
  def map(self, img):
    try:
      img.title = get_serving_url(img.file) if img.file else None
    except:
      return ([], [img])

    return ([img], []) # update/delete

class FixImages(BackendHandler):
  def get(self, **kwargs):
    # Mandamos a correr la tarea de mapeo
    tmp = ImageFixMapper()
    deferred.defer(tmp.run)
    self.response.write('corriendo ImageFixMapper')    

#------------
class RealEstateFixMapper(Mapper):
  KIND    = RealEstate
  def map(self, re):
    re.status     = RealEstate._ENABLED
    re.logo_url   = get_serving_url(re.logo) if re.logo else None
    re.plan       = Plan.all().get()
    re.domain_id  = do_slugify(re.name)
    
    return ([re], []) # update/delete

class FixRealEstates(BackendHandler):
  def get(self, **kwargs):
    # Mandamos a correr la tarea de mapeo
    tmp = RealEstateFixMapper()
    deferred.defer(tmp.run)
    self.response.write('corriendo RealEstateFixMapper')    

#------------
class PropertyFixMapper(Mapper):
  KIND    = Property
  def run(self):
    """Starts the mapper running."""
    self._continue(None, 100)

  def map(self, prop):
    
    try:
      prop.main_image_url = get_serving_url(prop.main_image) if prop.main_image else None
    except:
      prop.main_image_url = None
    
    prop.price_expensas = 0.0
    return ([prop], []) # update/delete

class FixProperty(BackendHandler):
  def get(self, **kwargs):
    # Mandamos a correr la tarea de mapeo
    tmp = PropertyFixMapper()
    deferred.defer(tmp.run)
    self.response.write('corriendo PropertyFixMapper')    
