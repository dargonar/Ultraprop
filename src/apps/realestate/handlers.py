# -*- coding: utf-8 -*-
import logging

from google.appengine.ext import db
from google.appengine.api import taskqueue
from google.appengine.api.images import get_serving_url

from webapp2 import cached_property

from models import Property
from backend_forms import PropertyFilterForm, PropertyContactForm

from utils import get_or_404, RealestateHandler

# Mail de bienvenida
from google.appengine.api import mail
from models import User

class LaunchEmail(RealestateHandler):
  def get(self, **kwargs):
    
    for e in User.all():
      
      # if e.email != 'matias.romeo@gmail.com':
        # continue
        
      realestate = e.realestate
      
      # Armo context, lo uso en varios lugares, jaja!
      context = { 'server_url':                 'http://www.ultraprop.com.ar'
                 ,'realestate_name':            realestate.name
                 ,'user_email':                 e.email
                 ,'user_password':              e.password
                 ,'support_url' :               'http://www.ultraprop.com.ar'}
      
      # Mando Correo a Usuario.
      # Armo el body en plain text.
      body = self.render_template('email/launch.txt', **context)  
      # Armo el body en HTML.
      html = self.render_template('email/launch.html', **context)  
      
      # Envío el correo.
      mail.send_mail(sender="www.ultraprop.com.ar <info@ultraprop.com.ar>" , 
                   to       = context['user_email'],
                   subject  = u"Actualización del sistema - ULTRAPROP",
                   body     = body,
                   html     = html)
      # --------------------------------------------------------------------------------
    
    self.response.write('Lito!')

# Redireccion por si alguien entra con url vieja
class Redirect(RealestateHandler):
  def get(self, **kwargs):
    realestate = self.request.GET['INM_Id']
    self.redirect_to('realestate/search', realestate=realestate)

# Index va a ser la homepage de la inmobiliaria, creo que quedará obsoleto.    
class Index(RealestateHandler):
  def get(self, **kwargs):
    realestate            = get_or_404(self.get_realestate_key_ex(kwargs.get('realestate')))
    kwargs['realestate']  = realestate
    kwargs['realestate_logo'] = get_serving_url(realestate.logo) if realestate.logo else None
    kwargs['menu_item']='index'
      
    return self.render_response('realestate/index.html', **kwargs)
 
# Info de la propiedad, creo que quedará obsoleto.    
class Info(RealestateHandler):
  def get(self, **kwargs):
    realestate            = get_or_404(self.get_realestate_key_ex(kwargs.get('realestate')))
    kwargs['realestate']  = realestate
    kwargs['realestate_logo'] = get_serving_url(realestate.logo) if realestate.logo else None
    kwargs['menu_item']   = 'info'
    kwargs['form']        =  self.form
    
    return self.render_response('realestate/contact.html', **kwargs)
  
  def post(self, **kwargs):
    self.request.charset = 'utf-8'
    realestate            = kwargs['realestate']
    
    if not self.form.validate():
      kwargs['flash'] = self.build_error('Verifique los datos ingresados:' + '<br/>'.join(reduce(lambda x, y: str(x)+' '+str(y), t) for t in self.form.errors.values()))
      
      return self.get(**kwargs)
    
    context = { 'realestate_key':           realestate            
                ,'sender_telephone':        self.form.telephone.data
                ,'sender_name':             self.form.name.data
                ,'sender_email':            self.form.email.data
                ,'sender_comment':          self.form.message.data
                ,'template_realestate':     1}               
                
    def txn():
      taskqueue.add(url=self.url_for('frontend/email_task'), params=dict({'action':'contact_user'}, **context))
      taskqueue.add(url=self.url_for('frontend/email_task'), params=dict({'action':'contact_agent'}, **context))
    
    db.run_in_transaction(txn)
    
    self.set_ok('Tu consulta enviada satisfactoriamente. Te hemos enviado una copia de la consulta a tu correo.')   
    return self.redirect_to('realestate/info', realestate=realestate)
    
  @cached_property
  def form(self):
    return PropertyContactForm(self.request.POST)