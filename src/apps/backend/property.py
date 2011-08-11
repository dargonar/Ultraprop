# -*- coding: utf-8 -*-
"""
    property handlers
    ~~~~~~~~
"""
from __future__ import with_statement

import logging
import unicodedata

from google.appengine.ext import db
from google.appengine.api import taskqueue

from webapp2 import cached_property, Response, RequestHandler

from backend_forms import PropertyForm, PropertyFilterForm
from models import Property, PropertyIndex, ImageFile
from search_helper_func import PropertyPaginatorMixin, create_query_from_dict

from utils import need_auth, BackendHandler 

class UpdateIndex(RequestHandler):
  # Solo se puede llamar desde appengine por eso no lo aseguramos
  # La configuracion esta en el app.yaml _ah/defered
  def post(self, **kwargs):
    key      = self.request.POST['key']
    action   = self.request.POST['action']
    property = db.get(key)
    oldpi    = PropertyIndex.all().filter('property =', db.Key(key)).get()
    
    # Necesita actualizar el indice
    if action == 'need_update':
      if oldpi:
        property.update_property_index(oldpi)
        oldpi.save()
      else:
        action = 'need_rebuild'
    
    if action == 'need_rebuild' or action == 'need_remove':
      if oldpi: oldpi.delete()
      if action == 'need_rebuild':
        pi = PropertyIndex(key_name = '%s,%f,%f' % (str(property.key()), property.location.lat, property.location.lon))
        property.update_property_index(pi)
        pi.put()
    
    self.response.write('ok')

class Restore(BackendHandler):
  
  @need_auth(code=404)
  def get(self, **kwargs):
    property = self.mine_or_404(kwargs['key'])
    property.status = Property._NOT_PUBLISHED
    property.save()
    
    self.response.write('ok')

class Remove(BackendHandler):
  
  @need_auth(code=404)
  def post(self, **kwargs):
    
    page      = int(self.request.POST['page'])
    newstatus = int(self.request.POST['newstatus'])
    
    keys = []
    for key in self.request.POST:
      if key != 'page' and key != 'newstatus':
        keys.append(key)
    
    properties = []
    for property in Property.get(keys):
      property.status  = newstatus
      property.save()
      
      # Verifico que sean mias las propiedades que voy a borrar del indice
      if str(property.realestate.key()) != self.get_realestate_key():
        self.abort(500)
      
      properties.append(property)
    
    # Salvamos y mandamos a remover del indice
    def savetxn():
      for key in keys:
        taskqueue.add(url=self.url_for('property/update_index'), params={'key': key,'action':'need_remove'})
    
    db.run_in_transaction(savetxn)
    
    self.set_ok('Las propiedades fueron %s correctamente' % ('recuperadas' if newstatus == Property._NOT_PUBLISHED else 'borradas') )
    return self.redirect_to('property/listpage', page=page)
    
class Publish(BackendHandler):
  
  @need_auth(code=404)
  def get(self, **kwargs):
    property = self.mine_or_404(kwargs['key'])
    property.status = Property._PUBLISHED if int(kwargs['yes']) else Property._NOT_PUBLISHED
    property.save()
    
    # Updateamos y mandamos a rebuild el indice si es necesario
    def savetxn():
      property.save()
      taskqueue.add(url=self.url_for('property/update_index'), params={'key': str(property.key()),'action':'need_rebuild' if property.status == Property._PUBLISHED else 'need_remove'})
    
    db.run_in_transaction(savetxn)
    return self.render_response('backend/includes/prop_list.html', property=property, Property=Property)
    
class Images(BackendHandler):
  
  @need_auth()
  def get(self, **kwargs):

    property = self.mine_or_404(kwargs['key'])
    images = ImageFile.all().filter('property =', property.key()).order('position')
    
    params = { 'current_tab' : 'pictures',
               'title'       : 'Imagenes de propiedad',
               'key'         :  kwargs['key'],
               'mnutop'      : 'propiedades',
               'images'      :  images}

    return self.render_response('backend/includes/pictures.html', **params)
    
class List(BackendHandler, PropertyPaginatorMixin):
  
  @need_auth()
  def get(self, **kwargs):
    return self.get2(**kwargs)
  
  @need_auth()
  def post(self, **kwargs):
    self.request.charset  = 'utf-8'
    return self.post2(**kwargs)

  def add_extra_filter(self, base_query):
    if not self.has_role('ultraadmin'):
      base_query.filter('realestate =', db.Key( self.get_realestate_key() ) )

    base_query.filter('status =', self.form.status.data)
      
      
  def render(self, **kwargs):
    kwargs['mnutop'] = 'propiedades'
    return self.render_response('backend/property_list.html', **kwargs)
    
class NewEdit(BackendHandler):
  
  @need_auth()
  def get(self, **kwargs):
    if 'key' in kwargs:
      kwargs['title'] = 'Editando Propiedad'
      kwargs['form']  = PropertyForm(obj=self.mine_or_404(kwargs['key']))
    else:
      kwargs['title'] = 'Nueva Propiedad'
      kwargs['form']  = self.form
    
    return self.show_property_form(**kwargs)
  
  @need_auth(code=404)
  def post(self, **kwargs):
    self.request.charset  = 'utf-8'
    
    editing = 'key' in self.request.POST and len(self.request.POST['key'])
    
    if not self.form.validate():
      kwargs['title'] = 'Editando Propiedad' if editing else 'Nueva Propiedad'
      kwargs['form']  = self.form
      kwargs['key']   = self.request.POST['key'] if editing else None
      kwargs['flash'] = {'message':'Verifique los datos ingresados', 'type':'error'}
      return self.show_property_form(**kwargs)
    
    # Actualizo o creo el model
    property = self.mine_or_404(self.request.POST['key']) if editing else Property.new(db.Key(self.get_realestate_key()))
    self.form.update_object(property)
    
    # Updateamos y mandamos a rebuild el indice si es necesario
    # Solo lo hacemos si se require y la propiedad esta publicada
    # Si se modifica una propiedad BORRADA o DESACTIVADA no se toca el indice por que no existe
    def savetxn():
      result = property.save() if editing else property.put()
      if result != 'nones' and property.status == Property._PUBLISHED:
        taskqueue.add(url=self.url_for('property/update_index'), params={'key': str(property.key()),'action':result})
    
    db.run_in_transaction(savetxn)
    
    if self.request.POST['goto'] == 'go':
      return self.redirect_to('property/images', key=str(property.key()))

    self.set_ok('La propiedad fue %s con exito' % ('modificada' if editing else 'creada') )    
    return self.redirect_to('property/listpage', page=1)

  def show_property_form(self, **kwargs):
      kwargs['current_tab'] = 'type'
      kwargs['mnutop']      = 'propiedades'  
      return self.render_response('backend/includes/form.html', **kwargs)
    
  @cached_property
  def form(self):
    return PropertyForm(self.request.POST)

# HACK DE AYUDA PARA EL UPLOAD iNICIAL    
from taskqueue import Mapper
from google.appengine.ext.blobstore import BlobInfo

class MyModelMapper(Mapper):
  KIND = User

  def map(self, e):
    
    if e.email != 'matias.romeo@gmail.com':
      return ([], []) 
    realestate            = e.realestate
    
    # Armo context, lo uso en varios lugares, jaja!
    context = { 'server_url':                 'http://'+self.request.headers.get('host', 'no host')
               ,'realestate_name':            realestate.name
               ,'user_email':                 e.email
               ,'user_password':              e.password
               , 'support_url' :               'http://'+self.request.headers.get('host', 'no host')}
    
    # Mando Correo a Usuario.
    # Armo el body en plain text.
    body = self.render_template('email/launch.txt', **context)  
    # Armo el body en HTML.
    html = self.render_template('email/launch.html', **context)  
    
    # Envío el correo.
    mail.send_mail(sender="www.ultraprop.com.ar <info@ultraprop.com.ar>" , 
                 to       = context['user_email'],
                 subject  = u"Actualización del sistema - ULTRAPROP",
                 body     = body,
                 html     = html)
    # --------------------------------------------------------------------------------
      
    
    return ([], [])

  def finish(self):
    logging.error('Terminamos...')

class RunMapper(BackendHandler):
  def get(self, **kwargs):
    from google.appengine.ext import deferred
    mapper = MyModelMapper()
    deferred.defer(mapper.run)
    self.response.write('Defereado!!')

class VerArchivo(BackendHandler):
  def get(self, **kwargs):
    return self.render_response(kwargs['archivo'].replace('-','/'))
    
class TraerFotines(RequestHandler):
  #@need_auth(roles='ultraadmin', code=505)
  def get(self, **kwargs):
    for p in Property.all(keys_only=True):
      taskqueue.add(url=self.url_for('traer_para'), params={'id': int(p.name())})

    self.response.write('listop')
    
class TraerPara(RequestHandler):
  def post(self, **kwargs):
    import urllib2
    id   = int(self.request.POST['id'])
    path ='http://www.ultraprop.com.ar/fotos_para.asp?id=%d' % id
    req  = urllib2.urlopen(path)
    try:
      for imgname in req:
        imgname = urllib2.quote(imgname[:-1])
        taskqueue.add(url=self.url_for('asignar_foto'), params={'id': id, 'imgname':imgname})
    except urllib2.URLError,e:
      logging.exception(e)
      logging.error('u:' + str(self.request.POST.mixed()))
    
    self.response.write('ok')

from google.appengine.api import images, files
from google.appengine.ext import db, blobstore
      
class AsignarFoto(RequestHandler):
  def post(self, **kwargs):
    import urllib2
    try:
      id       = int(self.request.POST['id'])
      imgname  = self.request.POST['imgname']
      path     = 'http://www.ultraprop.com.ar/fotos/%d/%s' % (id,imgname)
      property = Property.get_by_key_name(str(id))
      
      data = urllib2.urlopen(path).read()
      
      try:
        # Create the file
        file_name = files.blobstore.create(mime_type='image/jpg', _blobinfo_uploaded_filename=imgname)

        # Open the file and write to it
        img = images.Image(data)
        img.resize(width=800, height=600)

        
        with files.open(file_name, 'a') as f:
          f.write(img.execute_transforms(output_encoding=images.JPEG, quality=70))

        # Finalize the file. Do this before attempting to read it.
        files.finalize(file_name)

        # Get the file's blob key
        blob_key = files.blobstore.get_blob_key(file_name)
        imgfile = ImageFile()
        imgfile.title     = ''
        imgfile.data      = ''
        imgfile.file      = blob_key
        imgfile.filename  = imgname
        imgfile.realestate= property.realestate
        imgfile.property  = property
        imgfile.put()
        
        #Update property
        if property.images_count:
          property.images_count = property.images_count + 1
        else:
          property.images_count = 1
          property.main_image   = imgfile.file
        
        result = property.save()
      except Exception, e:
        logging.error(e)
        logging.error('--voy a retry--')
        self.response.status_int = 500
        return
        
      # if result != 'nones':
      #  taskqueue.add(url=self.url_for('property/update_index'), params={'key': str(property.key()),'action':result})
    except urllib2.URLError,e:
      logging.exception(e)
      try:
        logging.error('1:' + str(self.request.POST.mixed()))
      except:
        logging.error('--no pude1--' + str(id))
    except Exception, e:
      logging.exception(e)
      try:
        logging.error('2:' + str(self.request.POST.mixed()))
      except:
        logging.error('--no pude2--' + str(id))
      
    self.response.write('ok')