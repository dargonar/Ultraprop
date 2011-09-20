# -*- coding: utf-8 -*-
"""
    Help
    ~~~~~~~~
"""
import logging
from utils import need_auth, BackendHandler

class Index(BackendHandler):
  @need_auth(code=500)
  def get(self, **kwargs):
    return self.render_response('backend/help.html',mnutop='ayuda')