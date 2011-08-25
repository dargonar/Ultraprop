# -*- coding: utf-8 -*-
import logging

from google.appengine.api.images import get_serving_url

from utils import get_or_404, RealestateHandler
from search_helper_func import PropertyPaginatorMixin
from models import Property

class Search(RealestateHandler, PropertyPaginatorMixin):
  
  realestate = None
  
  def get(self, **kwargs):
    self.realestate = get_or_404( self.get_realestate_key_ex(kwargs.get('realestate')) )
    return self.get2(**kwargs)
  
  def post(self, **kwargs):
    self.request.charset = 'utf-8'
    self.realestate = get_or_404( self.get_realestate_key_ex(kwargs.get('realestate')) )
    return self.post2(**kwargs)

  def add_extra_filter(self, base_query):
    base_query.filter('status =', Property._PUBLISHED)
    base_query.filter('realestate =', self.realestate )

  def render(self, **kwargs):
    self.response.headers["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
    kwargs['menu_item']       = 'search'
    kwargs['realestate']      = self.realestate
    kwargs['realestate_logo'] = get_serving_url(self.realestate.logo) if self.realestate.logo else None
    
    return self.render_response('realestate/search.html', **kwargs)

