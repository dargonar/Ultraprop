# -*- coding: utf-8 -*-
"""
    Auth & RealState
    ~~~~~~~~
"""
from __future__ import with_statement

import logging

from google.appengine.api import files
from google.appengine.ext import db
from google.appengine.api import images 
from google.appengine.api.images import get_serving_url

from backend_forms import RealEstateForm 
from utils import get_or_404, need_auth, BackendHandler
from webapp2 import cached_property

class Edit(BackendHandler):
  #Edit/New
  @need_auth()
  def get(self, **kwargs):
    
    realestate                    = get_or_404(self.get_realestate_key())
    kwargs['form']                = RealEstateForm(obj=realestate)
    kwargs['key']                 = self.get_realestate_key()
    kwargs['mnutop']              = 'inmobiliaria'
    kwargs['realestate_logo']     = get_serving_url(realestate.logo) if realestate.logo else None
    return self.render_response('backend/realestate.html', **kwargs)
  
  #Create/Save RealEstate & User.
  @need_auth()
  def post(self, **kwargs):
    self.request.charset = 'utf-8'
    
    realestate = get_or_404(self.get_realestate_key())
    rs_validated = self.form.validate()
    if not rs_validated:
      kwargs['form']                = self.form
      kwargs['key']                 = self.get_realestate_key()
      kwargs['realestate_logo']     = get_serving_url(realestate.logo) if realestate.logo else None
      if self.form.errors:
        kwargs['flash']         = self.build_error(u'Verifique los datos ingresados:')
        # + '<br/>'.join(reduce(lambda x, y: str(x)+' '+str(y), t) for t in self.form.errors.values()))
      return self.render_response('backend/realestate.html', **kwargs)
    
    
    realestate = self.form.update_object(realestate)

    fs = self.request.POST['logo']
    if fs is not None and not isinstance(fs,unicode):
      if fs.filename is not None:
        # Create the file
        file_name = files.blobstore.create(mime_type='image/jpg', _blobinfo_uploaded_filename=fs.filename)
        # Open the file and write to it
        img = images.Image(fs.file.getvalue())
        
        # Validar ancho-alto
        # 125 max width, 380 max width
        
        img.rotate(0)
        with files.open(file_name, 'a') as f:
          data = img.execute_transforms(output_encoding=images.PNG)
          #logging.error('tipo:' + str(type(data)) + ':' + str(len(data)))
          
          f.write(data)
        # Finalize the file. Do this before attempting to read it.
        files.finalize(file_name)
        # Get the file's blob key
        blob_key            = files.blobstore.get_blob_key(file_name)
        
        realestate.logo      = blob_key
    
    realestate.save()
    
    # Actualizo los cambios en la sesi�n.
    self.do_login(db.get(self.get_user_key()))
    
    # Set Flash
    self.set_ok('Inmobiliaria guardada satisfactoriamente.')
    return self.redirect_to('backend/realestate/edit')
    
  @cached_property
  def form(self):
    return RealEstateForm(self.request.POST)