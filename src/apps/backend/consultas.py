# -*- coding: utf-8 -*-
"""
    Consultas
    ~~~~~~~~
"""
from __future__ import with_statement

import logging
import re

from google.appengine.ext import db

from utils import get_or_404, need_auth, BackendHandler
from models import RealEstate, Consulta, Property

    
class Index(BackendHandler):
  @need_auth()
  def get(self, **kwargs):
    realestate                    = get_or_404(self.get_realestate_key())
    query                         = Consulta.all().filter(' realestate = ', realestate.key()).order('-created_at')
    kwargs['consultas']           = query.fetch(1000)
    kwargs['mnutop']              = 'consultas'   
    kwargs['Property']            = Property
    return self.render_response('backend/consultas.html', **kwargs)
  