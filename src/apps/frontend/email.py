# -*- coding: utf-8 -*-
import logging
from google.appengine.ext import db
from google.appengine.api import mail

from webapp2 import abort, get_app # uri_for as url_for

from models import Property

from utils import get_bitly_url, MyBaseHandler

class SendTask(MyBaseHandler):
  
  def post(self, **kwargs):
    
    # TODO: Security hazard (think)
    params = self.request.POST.mixed()
    action = self.request.POST.get('action')
    getattr(self, action)(params)
    
    return
    
  def requestinfo_user(self, params):
    key                   = params['propery_key']
    property              = db.get(key) 
    realestate            = property.realestate 
    
    prop_operation_id     = params['prop_operation_id']
    
    realestate_property_link  = '%s/propiedades.html#%s/%s' % (realestate.website, key, prop_operation_id)
    if 'template_realestate' in params:
      property_link         = realestate_property_link
    else:
      str_query             = params['query_string'] 
      property_link         = get_bitly_url(str_query)
    
    
    if realestate.managed_domain==0:
      realestate_property_link = property_link
      
    # Armo context, lo uso en varios lugares, jaja!
    context = { 'server_url':                 'http://'+self.request.headers.get('host', 'no host')
               ,'realestate_name':            realestate.name
               ,'realestate_website':         realestate.website
               ,'realestate_property_link':   realestate_property_link
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
    
    # realestate_property_link  = '%s/propiedades.html#%s/%s' % (realestate.website, key, prop_operation_id)
    # if realestate.managed_domain==0:
      # realestate_property_link = property_link

    realestate_property_link  = '%s/propiedades.html#%s/%s' % (realestate.website, key, prop_operation_id)
    if 'template_realestate' in params:
      property_link         = realestate_property_link
    else:
      str_query             = params['query_string'] 
      property_link         = get_bitly_url(str_query)
    
    if realestate.managed_domain==0:
      realestate_property_link = property_link
    
    # Armo context, lo uso en varios lugares, jaja!
    context = { 'server_url':                 'http://'+self.request.headers.get('host', 'no host')
               ,'realestate_name':            realestate.name
               ,'realestate_website':         realestate.website
               ,'realestate_property_link':   realestate_property_link
               ,'property_link':              property_link
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
                 subject  = "Hicieron una consulta por un inmueble - ULTRAPROP",
                 body     = body,
                 html     = html)
    
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
               , 'support_url' :               'http://'+self.request.headers.get('host', 'no host')}
    
    # Mando Correo a Usuario.
    # Armo el body en plain text.
    body = self.render_template('email/'+self.config['ultraprop']['mail']['contact_agent']['template']+'.txt', **context)  
    # Armo el body en HTML.
    html = self.render_template('email/'+self.config['ultraprop']['mail']['contact_agent']['template']+'.html', **context)  
    
    # Envío el correo.
    mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['contact_agent']['sender'], 
                 to       = realestate.email,
                 subject  = "Hicieron una consulta - ULTRAPROP",
                 body     = body,
                 html     = html)
    # --------------------------------------------------------------------------------
      
    self.response.write('ok')