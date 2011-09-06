# -*- coding: utf-8 -*-
import logging
from google.appengine.ext import db
from google.appengine.api import mail

from webapp2 import abort, get_app # uri_for as url_for

from models import Property, Consulta

from utils import get_bitly_url, MyBaseHandler

class SendTask(MyBaseHandler):
  
  def post(self, **kwargs):
    self.request.charset = 'utf-8'
    
    # TODO: Security hazard (think)
    params = self.request.POST.mixed()
    action = self.request.POST.get('action')
    getattr(self, action)(params)
    
    return


  def common_context(self):
    context = { 'server_url':                 'http://'+self.request.headers.get('host', 'no host')
              , 'support_url' :               'http://'+self.request.headers.get('host', 'no host')}
    
  def trial_will_expire(self, params):
    logging.error('>>>>>>>>>>trial_will_expire')
  
  def trial_ended(self, params):
    logging.error('>>>>>>>>>>trial_ended')

  def no_payment(self, params):
    logging.error('>>>>>>>>>>no_payment')
  
  def enabled_again(self, params):
    logging.error('>>>>>>>>>>enabled_again')

  def payment_received(self, params):
    logging.error('>>>>>>>>>>payment_received')
    
  def new_invoice(self, params):
    logging.error('>>>>>>>>>>new_invoice')
    
  def requestinfo_user(self, params):
    key                   = params['propery_key']
    property              = db.get(key) 
    realestate            = property.realestate 
    
    prop_operation_id     = params['prop_operation_id']
    
    contact_from_map = True
    if 'template_realestate' in params:
      contact_from_map = False
    
    property_link  = '%s/propiedades.html#%s/%s' % (realestate.website, key, prop_operation_id)
    
    if contact_from_map:
      str_query                 = params['query_string'] 
      property_link             = get_bitly_url(str_query)
    
    
    # Armo context, lo uso en varios lugares, jaja!
    context = { 'server_url':                 'http://'+self.request.headers.get('host', 'no host')
               ,'realestate_name':            realestate.name
               ,'realestate_website':         realestate.website
               ,'property_link':              property_link
               ,'sender_name':                self.request.POST.get('sender_name')
               ,'sender_email':               self.request.POST.get('sender_email')
               ,'sender_comment':             self.request.POST.get('sender_comment')
               ,'prop_operation_id':          prop_operation_id
              , 'support_url' :               'http://'+self.request.headers.get('host', 'no host')}
    
    # Mando Correo a Usuario.
    # Armo el body en plain text.
    body = self.render_template('email/'+self.config['ultraprop']['mail']['requestinfo_user']['template']+'.txt', **context)  
    # Armo el body en HTML.
    html = self.render_template('email/'+self.config['ultraprop']['mail']['requestinfo_user']['template']+'.html', **context)  
    
    # Envío el correo.
    mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['requestinfo_user']['sender'], 
                 to       = context['sender_email'],
                 subject  = "Consulta por un inmueble - ULTRAPROP",
                 body     = body,
                 html     = html)
    # --------------------------------------------------------------------------------
      
    self.response.write('ok')
  
  def requestinfo_agent(self, params):  
    key                   = params['propery_key']
    property              = db.get(key) 
    realestate            = property.realestate 
    
    prop_operation_id     = params['prop_operation_id']
    
    contact_from_map = True
    if 'template_realestate' in params:
      contact_from_map = False
    
    realestate_property_link  = '%s/propiedades.html#%s/%s' % (realestate.website, key, prop_operation_id)
    
    if contact_from_map:
      if realestate.website is None or realestate.website.strip()=='': # Deben tener ptopiedades.html y rever tema #if realestate.managed_domain==1 :
        str_query                 = params['query_string'] 
        realestate_property_link  = get_bitly_url(str_query)
    
    # Armo context, lo uso en varios lugares, jaja!
    context = { 'server_url':                 'http://'+self.request.headers.get('host', 'no host')
               ,'realestate_name':            realestate.name
               ,'realestate_website':         realestate.website
               ,'realestate_property_link':   realestate_property_link
               ,'sender_name':                self.request.POST.get('sender_name')
               ,'sender_email':               self.request.POST.get('sender_email')
               ,'sender_comment':             self.request.POST.get('sender_comment')
               ,'sender_telephone':           self.request.POST.get('sender_telephone', None)
               ,'prop_operation_id':          prop_operation_id
              , 'support_url' :               'http://'+self.request.headers.get('host', 'no host')}
    
    # Mando Correo a agente.
    # Armo el body en plain text.
    body = self.render_template('email/'+self.config['ultraprop']['mail']['requestinfo_agent']['template']+'.txt', **context)  
    # Armo el body en HTML.
    html = self.render_template('email/'+self.config['ultraprop']['mail']['requestinfo_agent']['template']+'.html', **context)  
    
    # Envío el correo.
    mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['requestinfo_agent']['sender'], 
                 to       = realestate.email,
                 bcc      = self.config['ultraprop']['mail']['reply_consultas']['mail'],
                 subject  = "Hicieron una consulta por un inmueble - ULTRAPROP",
                 body     = body,
                 html     = html)
    
    self.save_consulta(property, realestate, contact_from_map, **context)
    
    self.response.write('ok')
    
    
  
  def contact_user(self, params):
    realestate_key        = params['realestate_key']
    realestate            = db.get(realestate_key) 
    
    # Armo context, lo uso en varios lugares, jaja!
    context = { 'server_url':                 'http://'+self.request.headers.get('host', 'no host')
               ,'realestate_name':            realestate.name
               ,'realestate_website':         realestate.website
               ,'sender_name':                self.request.POST.get('sender_name')
               ,'sender_email':               self.request.POST.get('sender_email')
               ,'sender_comment':             self.request.POST.get('sender_comment')
               , 'support_url' :               'http://'+self.request.headers.get('host', 'no host')}
    
    # Mando Correo a Usuario.
    # Armo el body en plain text.
    body = self.render_template('email/'+self.config['ultraprop']['mail']['contact_user']['template']+'.txt', **context)  
    # Armo el body en HTML.
    html = self.render_template('email/'+self.config['ultraprop']['mail']['contact_user']['template']+'.html', **context)  
    
    # Envío el correo.
    mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['contact_user']['sender'], 
                 to       = context['sender_email'],
                 subject  = "Consulta - ULTRAPROP",
                 body     = body,
                 html     = html)
    # --------------------------------------------------------------------------------
      
    self.response.write('ok')
    
  
  def contact_agent(self, params):
    realestate_key        = params['realestate_key']
    realestate            = db.get(realestate_key) 
    
    # Armo context, lo uso en varios lugares, jaja!
    context = { 'server_url':                 'http://'+self.request.headers.get('host', 'no host')
               ,'realestate_name':            realestate.name
               ,'realestate_website':         realestate.website
               ,'sender_name':                self.request.POST.get('sender_name')
               ,'sender_email':               self.request.POST.get('sender_email')
               ,'sender_comment':             self.request.POST.get('sender_comment')
               ,'sender_telephone':           self.request.POST.get('sender_telephone')
               ,'support_url' :               'http://'+self.request.headers.get('host', 'no host')}
    
    # Mando Correo a Usuario.
    # Armo el body en plain text.
    body = self.render_template('email/'+self.config['ultraprop']['mail']['contact_agent']['template']+'.txt', **context)  
    # Armo el body en HTML.
    html = self.render_template('email/'+self.config['ultraprop']['mail']['contact_agent']['template']+'.html', **context)  
    
    # Envío el correo.
    mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['contact_agent']['sender'], 
                 to       = realestate.email,
                 bcc      = self.config['ultraprop']['mail']['reply_consultas']['mail'],
                 subject  = "Hicieron una consulta - ULTRAPROP",
                 body     = body,
                 html     = html)
    
    self.save_consulta(None, realestate, False, **context)
    
    self.response.write('ok')
    
  
  def save_consulta(self, property, realestate, contact_from_ultraprop, **context):
    #logging.debug('save_consulta:: llamada')          
    try:
      consulta                            = Consulta()
      consulta.realestate_name            = context['realestate_name']
      consulta.realestate                 = realestate
      consulta.property                   = property
      
      consulta.realestate_property_link   = ''
      if 'realestate_property_link' in context:
        consulta.realestate_property_link = context['realestate_property_link']
      
      consulta.property_link              = ''
      if 'property_link' in context:
        consulta.property_link            = context['property_link']
        
      consulta.sender_name                = context['sender_name']
      consulta.sender_email               = context['sender_email']
      consulta.sender_comment             = context['sender_comment']
      consulta.sender_telephone           = ''
      if 'sender_telephone' in context:
        consulta.sender_telephone         = context['sender_telephone']
      
      prop_operation_id                   = int(context['prop_operation_id']) if 'prop_operation_id' in context else 0
      consulta.prop_operation_desc = ''
      if prop_operation_id == Property._OPER_SELL:
        consulta.prop_operation_desc = 'Venta'
      if prop_operation_id == Property._OPER_RENT:
        consulta.prop_operation_desc = 'Alquiler'
      
      consulta.is_from_ultraprop          = 1 if contact_from_ultraprop else 0
      consulta.save()
    except Exception, e:
      logging.error('email.py::save_consulta() exception.')
      logging.exception(e)
    return 'ok'