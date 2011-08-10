# -*- coding: utf-8 -*-
import logging

from webapp2_extras.json import json
from search_helper import config_array, MAX_QUERY_RESULTS
from utils import FrontendHandler
from models import Property

class Index(FrontendHandler):
  def get(self, **kwargs):
    
    if not self.session.has_key('frontend.querystring'):
      show_extended_filter = self.request.GET.get('filtro_extendido',default=0)
      dict = {}
      for key in self.request.GET.keys():
        value = self.request.GET.get(key)
        if value is not None: # and len(str(value))>0:
          dict[key] = value
      dict['prop_operation_id']     = str(Property._OPER_SELL)
      dict['show_extended_filter']  = show_extended_filter
      if self.session.has_key('map.filter.realestate'):
        dict['map.filter.realestate'] = self.session.pop('map.filter.realestate')
    else:
      dict = self.session.pop('frontend.querystring') #self.session.clear()
      
    return self.render_response('frontend/index.html'
                          , config_arrayJSON=json.dumps(config_array)
                          , config_array=config_array
                          , max_results=MAX_QUERY_RESULTS
                          , preset=dict
                          , presetJSON=json.dumps(dict)
                          , _OPER_SELL=Property._OPER_SELL
                          , _OPER_RENT=Property._OPER_RENT)

  def post(self, **kwargs):
    dict = {}
    for key in self.request.POST.keys():
      value = self.request.POST.get(key)
      if value is not None and len(value)>0:
        dict[key] = value
    self.session['frontend.querystring'] = dict
    
    return self.redirect_to('frontend/map')

  def realesate_filtered(self, **kwargs):
    self.session['map.filter.realestate'] = kwargs['realestate']
    return self.redirect_to('frontend/map')