# -*- coding: utf-8 -*-
"""
    Auth & RealState
    ~~~~~~~~
"""
from __future__ import with_statement

import logging

from google.appengine.ext import db
from google.appengine.api import mail

from webapp2 import cached_property

from backend_forms import RealEstateWebSiteForm, validate_domain_id
from utils import get_or_404, need_auth, BackendHandler
from models import RealEstate


class CheckDomainId(BackendHandler):
  @need_auth()
  def get(self, **kwargs):
    self.request.charset = 'utf-8'
    domain_id = self.request.GET['did'].strip()
    
    res = validate_domain_id(domain_id, self.get_realestate_key())
    return self.render_json_response(res)
    
class Edit(BackendHandler):
  #Edit/New
  @need_auth()
  def get(self, **kwargs):
    
    realestate                    = get_or_404(self.get_realestate_key())
    kwargs['form']                = RealEstateWebSiteForm(obj=realestate)
    kwargs['key']                 = self.get_realestate_key()
    kwargs['realestate']          = realestate
    kwargs['mnutop']              = 'website'
   
    return self.render_response('backend/realestate_website.html', **kwargs)
  
  #Create/Save RealEstate & User.
  @need_auth()
  def post(self, **kwargs):
    self.request.charset = 'utf-8'
    
    realestate = get_or_404(self.get_realestate_key())
    
    #HACK: Hack? le pongo un miembro para que la validacion del slug sepa cual es la key actual de la RealEste
    #de otra forma va a decir que ya esta siendo utilizada
    self.form.thekey = self.get_realestate_key()
    
    rs_validated = self.form.validate()
    if not rs_validated:
      kwargs['form']                = self.form
      kwargs['key']                 = self.get_realestate_key()
      if self.form.errors:
        kwargs['flash']         = self.build_error(u'Verifique los datos ingresados:')
        # + '<br/>'.join(reduce(lambda x, y: str(x)+' '+str(y), t) for t in self.form.errors.values()))
      return self.render_response('backend/realestate_website.html', **kwargs)
    
    
    realestate, requested_hosting = self.form.update_object(realestate)
    
    realestate.save()
    
    if requested_hosting:
      mail_to='info@ultraprop.com.ar'
      body='La inmobiliaria %s desea %shostearse en ULTRAPROP. Key: %s; - Name:%s; - Url:%s' % (realestate.name, 'DES' if realestate.managed_domain==0 else '',str(realestate.key()), realestate.name, self.url_for( 'realestate/search', _full=True, realestate=str(realestate.key())))
      mail.send_mail(sender="www.ultraprop.com.ar <info@ultraprop.com.ar>", 
                   to       = mail_to,
                   subject  = "ULTRAPROP: Una inmobiliaria cambio su estado de hosting en ULTRAPROP",
                   body     = body)
    
    # Actualizo los cambios en la sesión.
    self.do_login(db.get(self.get_user_key()))
    
    # Set Flash
    self.set_ok('configuración de Sitio Web guardado satisfactoriamente. Un agente de ULTRAPROP se comunicará con Ud. en breve.' )
    return self.redirect_to('backend/realestate_website/edit')
    
  @cached_property
  def form(self):
    return RealEstateWebSiteForm(self.request.POST)