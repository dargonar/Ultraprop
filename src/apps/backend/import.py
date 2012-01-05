# -*- coding: utf-8 -*-
"""
    property handlers
    ~~~~~~~~
"""
from __future__ import with_statement

import logging

from google.appengine.ext import db
from google.appengine.api import taskqueue

from webapp2 import cached_property, Response, RequestHandler

class InmoBusqueda(RequestHandler):
  def get(self, **kwargs):
    inmoid = kwargs['inmoid']
    
