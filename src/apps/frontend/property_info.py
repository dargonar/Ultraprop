# -*- coding: utf-8 -*-
import logging
from google.appengine.api import taskqueue
from google.appengine.ext import db
from google.appengine.api import mail

from webapp2 import abort, get_app, cached_property # uri_for as url_for

from search_helper import config_array
from models import Property, ImageFile

from utils import get_or_404, FrontendHandler, get_bitly_url
from backend_forms import PropertyContactForm

class PopUp(FrontendHandler):
  def get(self, **kwargs):
    
    key                   = kwargs['key']
    bubble_css            = kwargs['bubble_css']
    price_data_operation  = int(kwargs['oper'])
    property              = get_or_404(key)
    
    images = ImageFile.all().filter('property =', db.Key(key)).order('position')
    context = {'images':images, 'property': property, 'Property':Property, 'bubble_css':bubble_css, 'price_data_operation':price_data_operation}
    
    return self.render_response('frontend/templates/_bubble.html', **context)  
    
class Ficha(FrontendHandler):
  def get(self, **kwargs):
    
    key                   = kwargs['key']
    price_data_operation  = kwargs['oper']
    
    property              = get_or_404(key) 
    
    price                 = property.price_sell 
    cur                   = property.price_sell_currency 
    
    if int(price_data_operation) ==  Property._OPER_RENT: 
      price  = property.price_rent  
      cur    = property.price_rent_currency 

    context = { 'property': property
              , 'Property':Property
              , 'price':price
              , 'cur':cur
              , 'config_array':config_array
              , 'price_data_operation':price_data_operation}
    
    
    context_ex = dict({'form':self.form}, **context)
    context_ex = dict({'images': ImageFile.all().filter('property =', db.Key(key)).order('position') }, **context_ex)
    
    ficha = self.render_template('frontend/templates/_ficha.html', **context_ex)  
    tab   = self.render_template('frontend/templates/_prop_tab.html', **context)
    
    return self.render_json_response({'ficha': ficha, 'tab': tab})
  
  @cached_property
  def form(self):
    return PropertyContactForm()
  
  
class Compare(FrontendHandler):
  def get(self, **kwargs):
    
    return self.render_response('frontend/compare.html'
                          , config_array=config_array
                          , preset={})

    
class SendMail(FrontendHandler):
  def post(self, **kwargs):
    self.request.charset = 'utf-8'
    
    key                   = kwargs['key']
    
    if not self.form.validate():
      # responsetxt = [reduce(lambda x, y: str(x)+' '+str(y), t) for t in self.form.errors.values()]
      responsetxt = 'Verifique los datos ingresados:' + '<br/>'.join(reduce(lambda x, y: str(x)+' '+str(y), t) for t in self.form.errors.values())
      self.response.status_int = 500
      self.response.write(responsetxt)
      return
    
    context = { 'propery_key':                key
               ,'query_string':               self.request.query_string + '&version=1'       
               ,'sender_name':                self.form.name.data
               ,'sender_email':               self.form.email.data
               ,'sender_comment':             self.form.message.data
               ,'prop_operation_id':          self.request.POST.get('prop_operation_id', default='1')}               
                
    def txn():
      taskqueue.add(url=self.url_for('frontend/email_task'), params=dict({'action':'requestinfo_user'}, **context))
      taskqueue.add(url=self.url_for('frontend/email_task'), params=dict({'action':'requestinfo_agent'}, **context))
    
    db.run_in_transaction(txn)
    
    self.response.write('Tu consulta enviada satisfactoriamente. Te hemos enviado una copia de la consulta a tu correo.')  
    
  @cached_property
  def form(self):
    return PropertyContactForm(self.request.POST)