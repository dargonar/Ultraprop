# -*- coding: utf-8 -*-
"""
    Auth & RealState
    ~~~~~~~~
"""
from __future__ import with_statement

import logging
import re

from google.appengine.ext import db
from google.appengine.api import mail

from utils import get_or_404, need_auth, BackendHandler
from models import RealEstate


    
class Demo(BackendHandler):
  #Edit/New
  @need_auth()
  def get(self, **kwargs):
    kwargs['mnutop']              = 'realestatebook'
    realestate                    = get_or_404(self.get_realestate_key())
    kwargs['realestates']         = RealEstate.all().fetch(100)
    return self.render_response('backend/realestatebook.html', **kwargs)

class WantsPoke(BackendHandler):
  #Edit/New
  @need_auth()
  def get(self, **kwargs):
    
    realestate                    = get_or_404(self.get_realestate_key())
    mail_to='info@ultraprop.com.ar'
    body='La inmobiliaria %s desea el feature INMOBILIARIAS AMIGAS en ultraprop. Key: %s; - Name:%s; - Url:%s' %  (realestate.name, str(realestate.key()), realestate.name, self.url_for( 'realestate/search', _full=True, realestate=str(realestate.key())))
    mail.send_mail(sender="www.ultraprop.com.ar <info@ultraprop.com.ar>", 
                 to       = mail_to,
                 subject  = "ULTRAPROP: Una inmobiliaria quiere INMOBILIARIAS AMIGAS",
                 body     = body)
    
    self.set_ok('Su pedido fue recibido.')
    
    return self.redirect_to('backend/realestatebook/list')
