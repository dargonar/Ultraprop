# -*- coding: utf-8 -*-
import logging

from google.appengine.ext import db
from google.appengine.api import taskqueue
from google.appengine.api.images import get_serving_url

from webapp2 import cached_property

from models import Property, ImageFile, RealEstate
from search_helper import config_array
from backend_forms import PropertyFilterForm, PropertyContactForm

from utils import get_or_404, RealestateHandler
    
class Show(RealestateHandler):
  def get(self, **kwargs):
    
    realestate = get_or_404(self.get_realestate_key_ex(kwargs.get('realestate')))
    
    # Ponemos la pantalla de disabled si esta en NO_PAYMENT
    if realestate.status == RealEstate._NO_PAYMENT:
      return self.render_response('realestate/disabled.html', realestate=realestate)
    
    kwargs['realestate']  = realestate
    kwargs['realestate_logo'] =  realestate.logo_url
    
    key                   = kwargs['key']
    price_data_operation  = kwargs['oper']
    
    property = db.get(key) 
    
    price            = property.price_sell 
    cur              = property.price_sell_currency 
    
    if int(price_data_operation) ==  Property._OPER_RENT: 
      price  = property.price_rent  
      cur    = property.price_rent_currency 

    kwargs['property']    = property
    kwargs['Property']    = Property
    kwargs['price']       = price
    kwargs['cur']         = cur
    kwargs['config_array']= config_array
    kwargs['menu_item']   =  'ficha'
    
    kwargs['form']        =  self.form
    kwargs['oper']        =  price_data_operation
    
    kwargs['images']      = ImageFile.all().filter('property =', db.Key(key)).order('position');
    
    return self.render_response('realestate/_ficha.html', **kwargs)
  
  def post(self, **kwargs):
    self.request.charset  = 'utf-8'
  
    key                   = kwargs['key']
    realestate            = kwargs['realestate']
    prop_operation_id     = kwargs['oper']
    
    if not self.form.validate():
      kwargs['flash'] = self.build_error('Verifique los datos ingresados:' + '<br/>'.join(reduce(lambda x, y: str(x)+' '+str(y), t) for t in self.form.errors.values()))
      
      return self.get(**kwargs)
    
    context = { 'propery_key':                key
               ,'realestate_key':             realestate
               ,'sender_name':                self.form.name.data
               ,'sender_email':               self.form.email.data
               ,'sender_comment':             self.form.message.data
               ,'sender_telephone':           self.form.telephone.data
               ,'template_realestate':        1
               ,'prop_operation_id':          prop_operation_id}               
                
    def txn():
      taskqueue.add(url=self.url_for('backend/email_task'), params=dict({'action':'requestinfo_user'}, **context), transactional=True)
      taskqueue.add(url=self.url_for('backend/email_task'), params=dict({'action':'requestinfo_agent'}, **context), transactional=True)
    
    db.run_in_transaction(txn)
    
    self.set_ok('Tu consulta fue enviada satisfactoriamente. Te hemos enviado una copia de la consulta a tu correo.')  
    return self.redirect_to('realestate/ficha', key=key, oper=prop_operation_id, realestate=realestate)
    
  @cached_property
  def form(self):
    return PropertyContactForm(self.request.POST)