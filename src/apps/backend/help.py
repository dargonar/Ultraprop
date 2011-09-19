# -*- coding: utf-8 -*-
"""
    Help
    ~~~~~~~~
"""
import logging
from utils import need_auth

class Index(BackendHandler):
  @need_auth
  def get(self, **kwargs):
    return self.render_response('backend/help.html')