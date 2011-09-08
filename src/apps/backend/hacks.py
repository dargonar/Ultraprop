# -*- coding: utf-8 -*-
"""
    hacks handlers
    ~~~~~~~~
"""

import logging
from datetime import datetime, date
from google.appengine.api.images import get_serving_url
from google.appengine.ext import deferred, db, blobstore

# Cositas sueltas
from utils import get_or_404, need_auth, BackendHandler 
from taskqueue import Mapper
from models import Property, ImageFile, RealEstate, Plan, RealEstate, Invoice, PropertyIndex, User
from myfilters import do_slugify
from apps.backend.payment import create_transaction_number

from google.appengine.api import taskqueue

class Unsubscribe(BackendHandler):
  def get(self, **kwargs):
    return self.render_response('backend/unsubscribe.html', email=kwargs['email'])

class LaPlataCampaign(BackendHandler):
  def get(self, **kwargs):
    emails = [
      'info@daufi.com.ar',
      'info@grupo-urbano.com.ar',
      'info@buildinginmobiliaria.com',
      'consultas@marcelojalilycia.com.ar',
      'info@penayopropiedades.com.ar',
      'info@cortipropiedades.com.ar',
      'info@marenaprop.com.ar',
      'contacto@franciscoinmob.com.ar',
      'consultas@tempesta.com.ar',
      'info@bellagamba.com',
      'info@silviaposca.com.ar',
      'info@camuscentro.com.ar',
      'info@siluscapital.com',
      'info@agostinelli.com.ar',
      'info@alvarezprop.com.ar',
      'info@oterorossi.com.ar',
      'info@danieljakus.com.ar',
      'info@dacal.com.ar',
      'info@rivaspropiedades.com.ar',
      'info@valverdepropiedades.com.ar',
      'info@depinagaramon.com.ar',
      'info@capitalpropiedades.com.ar',
      'info@estudiomandon.com.ar',
      'info@horaciovarela.com',
      'ventas@incopropiedades.com.ar',
      'ventas@jjyacoub.com.ar',
      'administracion@jjyacoub.com.ar',
      'info@danieljuarez.com.ar',
      'info@betancorpropiedades.com.ar',
      'info@andreatava.com.ar',
      'info@andreatava.com.ar',
      'info@menachopropiedades.com.ar',
      'info@ringueletprop.com.ar',
      'info@debonapropiedades.com.ar',
      'info@lundin.com.ar',
      'consultas@romeropropiedades.com',
      'info@urquiza.com.ar',
      'consultas@mooneybienesraices.com.ar',
      'info@gruporandrup.com.ar',
      'info@mirtalibera.com.ar',
      'info@montesantiprop.com.ar',
      'info@verainmobiliaria.com.ar',
      'consultas@montesantiprop.com.ar',
      'info@tapiamartinoli.com.ar',
      'info@donatteri.com.ar',
      'info@ramospropiedades.com.ar',
      'consultas@axionpropiedades.com.ar',
      'info@boscpropiedades.com.ar',
      'info@vendodpto.com.ar',
      'admin@cambroneroinmuebles.com.ar',
      'info@cantisanoprop.com.ar',
      'info@estudiomgherrera.com.ar',
      'info@francopropiedadeslp.com',
      'info@inmobiliariavision.com',
      'contacto@dinardopropiedades.com.ar',
      'contacto@villalvapropiedades.com.ar',
      'info@licainmobiliaria.com.ar',
      'info@javiermoragues.com',
      'info@speranzapropiedades.com.ar',
      'info@laplatapropiedades.net',
      'info@marianopasini.com.ar',
      'info@mirtalibera.com.ar',
      'consultas@mooneybienesraices.com.ar',
      'info@nicolasmoron.com.ar',
      'info@patriciabellotti.com.ar',
      'info@grupomorenolp.com.ar',
      'info@tapiamartinoli.com.ar',
      'consultas@urquiza.com.ar',
      'info@juradobienesraices.com.ar',
      'info@andreatava.com.ar',
      'contacto@carinopropiedades.com.ar',
      'info@ceciliacordero.com.ar',
      'info@dedich.com.ar']
    
    # emails = ['ptutino@gmail.com', 'ptutino@gmail.com']
    sent = []
    for email in emails:
      if email in sent:
        continue
      params = {'action': 'laplata_campaign', 'email':email}
      taskqueue.add(url='/tsk/email_task', params=params)
      sent.append(email)
      
    
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

class RemoveRealEstate(BackendHandler):
  def get(self, **kwargs):
    re = get_or_404(kwargs['key'])
    
    blobs = []
    imgs  = []
    props = []
    
    for img in ImageFile.all().filter('realestate', re.key()):
      blobs.append(img.file.key())
      imgs.append(img.key())
      props.append(img.property.key())
      
    blobstore.delete(blobs)
    db.delete(props)
    db.delete(imgs)

    pis = []
    for pi in PropertyIndex.all().filter('realestate', re.key()):
      pis.append(pi.key())
      
    db.delete(pis)
    
    invs = []
    pays = []
    for inv in Invoice.all().filter('realestate', re.key()):
      invs.append(inv)
      if inv.payment:
        pays.append(inv.payment.key())
    
    db.delete(invs)
    db.delete(pays)
    
    usrs = []
    for usr in User.all().filter('realestate', re.key()):
      usrs.append(usr)
    
    db.delete(usrs)
    
    re.delete()
    
    self.response.write('borrado %s' % kwargs['key'])
    
    

# -----------------------------Mappers para 1.2 --------------------

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
    
    #re.status     = RealEstate._ENABLED
    #re.logo_url   = get_serving_url(re.logo) if re.logo else None
    #re.plan       = Plan.all().get()
    #re.domain_id  = do_slugify(re.name)

    first_date = date(2011,9,10)
    
    invoice = Invoice()
    invoice.realestate = re
    invoice.trx_id     = create_transaction_number(first_date, re)
    invoice.amount     = re.plan.amount
    invoice.state      = Invoice._NOT_PAID
    invoice.date       = first_date
    invoice.put()

    # Nuevo hack
    re.managed_domain = 1
    re.last_invoice   = invoice.date
    re.last_login     = datetime.now()
    
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
