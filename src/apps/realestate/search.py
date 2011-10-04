# -*- coding: utf-8 -*-
import logging

from google.appengine.api.images import get_serving_url

from utils import get_or_404, RealestateHandler
from search_helper_func import PropertyPaginatorMixin
from models import Property, RealEstate

class Search(RealestateHandler, PropertyPaginatorMixin):
  
  realestate = None
  
  def get(self, **kwargs):
    self.realestate = get_or_404( self.get_realestate_key_ex(kwargs.get('realestate')) )

    # Ponemos la pantalla de disabled si esta en NO_PAYMENT
    if self.realestate.status == RealEstate._NO_PAYMENT:
      return self.render_response('realestate/disabled.html', realestate=self.realestate)
      
    return self.get2(**kwargs)
  
  def by_slug(self, **kwargs):
    
    self.realestate = RealEstate.all().filter(' domain_id = ', kwargs.get('realestate_slug')).get()

    # Ponemos la pantalla de disabled si esta en NO_PAYMENT
    if self.realestate.status == RealEstate._NO_PAYMENT:
      return self.render_response('realestate/disabled.html', realestate=self.realestate)
      
    return self.get2(**kwargs)
  
  def post(self, **kwargs):
    self.request.charset = 'utf-8'
    self.realestate = get_or_404( self.get_realestate_key_ex(kwargs.get('realestate')) )
      
    # Ponemos la pantalla de disabled si esta en NO_PAYMENT
    if self.realestate.status == RealEstate._NO_PAYMENT:
      return self.render_response('realestate/disabled.html', realestate=self.realestate)
    
    return self.post2(**kwargs)

  def add_extra_filter(self, base_query):
    base_query.filter('status =', Property._PUBLISHED)
    # base_query.filter('realestate =', self.realestate )
    base_query.filter('location_geocells =', RealEstate.get_realestate_sharing_key(None, self.realestate))

  def render(self, **kwargs):
    self.response.headers["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
    kwargs['menu_item']       = 'search'
    kwargs['realestate']      = self.realestate
    kwargs['realestate_logo'] =  self.realestate.logo_url
    if 'page' not in kwargs:
      kwargs['page'] = 1
    return self.render_response('realestate/search.html', **kwargs)

