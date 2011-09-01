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
