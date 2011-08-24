# -*- coding: utf-8 -*-
"""
    Auth & RealState
    ~~~~~~~~
"""
import logging
from google.appengine.api import mail

from webapp2 import cached_property
from backend_forms import SignUpForm
from models import RealEstate, User
from utils import get_or_404, BackendHandler

class Index(BackendHandler):
  def get(self, **kwargs):
    if self.is_logged and self.is_enabled:
      if self.is_realestate_enabled:
        return self.redirect_to('property/list')
      else:
        return self.redirect_to('backend/realestate/edit')
    return self.redirect_to('backend/auth/login')
    
class Login(BackendHandler):
  def get(self, **kwargs):
    flashes           = self.session.get_flashes()
    kwargs['flash']   = flashes[0][0] if len(flashes) and len(flashes[0]) else None
    self.session.clear()  
    return self.render_response('backend/login.html', **kwargs)
  
  def post(self, **kwargs):
    self.request.charset  = 'utf-8'
    
    password  = self.request.POST.get('userpass')
    email     = self.request.POST.get('useremail')
    
    user      = User.all().filter('email =', email).filter('password =', password).get()
    
    if not user:
      kwargs['flash'] = self.build_error(u'Correo o contraseña incorrectos')
      return self.render_response('backend/login.html', **kwargs)
    
    if user.enabled!=1:
      kwargs['flash'] = self.build_error(u'Debe validar su correo electrónico ')
      return self.render_response('backend/login.html', **kwargs)
      
    self.do_login(user)
    
    if not self.is_realestate_enabled:
      self.set_info('Debe configurar la inmobiliaria para comenzar a operar.')
      return self.redirect_to('backend/realestate/edit')
    return self.redirect_to('property/list')
    
class Logout(BackendHandler):
  def get(self, **kwargs):
    self.session.clear()  
    return self.redirect_to('backend/auth/login')
    
class SignUp(BackendHandler):
  #Edit/New
  def get(self, **kwargs):
    
    if self.is_logged:
      return self.redirect_to('backend/realestate/edit')
    
    kwargs['form']   = self.form
    return self.render_response('backend/signup.html', **kwargs)
  
  #Create/Save RealEstate & User.
  def post(self, **kwargs):
    self.request.charset  = 'utf-8'
    
    form_validated = self.form.validate()
    if not form_validated:
      kwargs['form']         = self.form
      if self.form.errors:
        kwargs['flash']      = self.build_error('Verifique los datos ingresados:')# + '<br/>'.join(reduce(lambda x, y: str(x)+' '+str(y), t) for t in self.user_form.errors.values()))
      
      return self.render_response('backend/signup.html', **kwargs)
    
    realEstate = RealEstate.new()
    realEstate.name   = self.form.name.data
    realEstate.email  = self.form.email.data
    realEstate.put()
    
    user = User.new()
    user.email            = self.form.email.data
    user.password         = self.form.password.data
    user.rol              = 'owner'
    
    # Asigno inmobiliaria al Usuario.
    user.realestate = realEstate
    
    # Salvo los objetos.
    user.put()
    
    # Mando Correo de bienvenida y validación de eMail.
    # Armo el contexto dado que lo utilizo para mail plano y mail HTML.
    context = { 'server_url':         'http://'+self.request.headers.get('host', 'no host')
              , 'realestate_name':    realEstate.name
              , 'validate_user_link': self.url_for('backend/validate/user', key=str(user.key()), _full=True) 
              , 'support_url' :       'http://'+self.request.headers.get('host', 'no host')}
    
    # Armo el body en plain text.
    body = self.render_template('email/'+self.config['ultraprop']['mail']['signup']['template']+'.txt', **context)  
    # Armo el body en HTML.
    html = self.render_template('email/'+self.config['ultraprop']['mail']['signup']['template']+'.html', **context)  
    
    # Envío el correo.
    mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['signup']['sender'], 
                 to=user.email,
                 subject="ULTRAPROP - Bienvenido",
                 body=body,
                 html=html
                 )
                 
    self.set_ok(u'Un correo ha sido enviado a su casilla de email. Ingrese a ULTRAPROP a través del enlace recibido.')
    
    return self.redirect_to('backend/auth/login')
    
  @cached_property
  def form(self):
    return SignUpForm(self.request.POST)

class ValidateUser(BackendHandler):
  def get(self, **kwargs):
    user = get_or_404(kwargs.get('key'))
    if user.enabled>0:
      return self.redirect_to('backend/auth/login')
    
    user.enabled = 1
    user.save()
    
    self.do_login(user)
    
    self.set_ok('Su correo ha sido validado. Por favor complete la información de la inmobiliaria para comenzar a operar con ULTRAPROP.<br/> Si no encuentra el correo en INBOX, búsquelo en SPAM.')
    
    return self.redirect_to('backend/realestate/edit')

class UnRestorePassword(BackendHandler):
  def get(self, **kwargs):
    user              = get_or_404(kwargs.get('key'))
    if user.enabled == 0 and user.restore_password == 1:
      user.restore_password = 0
      user.enabled = 1
      user.save()
    self.set_ok('Su cuenta ha sido actualizada satisfactoriamente!')
    return self.redirect_to('backend/auth/login')    
    
class RestorePassword(BackendHandler):
  def get(self, **kwargs):
    user                = get_or_404(kwargs.get('key'))
    
    if user.enabled != 0 or user.restore_password != 1:
      return self.render_response('error.html', code=404, text='No está habilitado para ejecutar este comando.' )
    
    kwargs['key']       = str(user.key())
    kwargs['email']     = user.email
    return self.render_response('backend/restore_password.html', **kwargs)
  
  def post(self, **kwargs):
    self.request.charset  = 'utf-8'
    
    user               = get_or_404(kwargs.get('key'))
    
    email             = self.request.POST.get('useremail', default=None)
    password          = self.request.POST.get('password', default=None)
    confirm_password  = self.request.POST.get('confirm', default=None)
    
    if user.email != email:
      self.set_error('Verifique el correo electrónico.')
      return self.redirect_to('/restore/password/'+str(user.key()))
      
    if password != confirm_password:
      self.set_error('Las contraseñas no son iguales.')
      return self.redirect_to('/restore/password/'+str(user.key()))
    
    user.password         = password
    user.restore_password = 0             
    user.enabled          = 1
    user.save()
    
    self.set_ok(u'Su contraseña ha sido modificada satisfactoriamente.')
    
    return self.redirect_to('backend/auth/login')    
    
class RestorePasswordRequest(BackendHandler):
  def post(self, **kwargs):
    self.request.charset  = 'utf-8'
    
    email     = self.request.POST.get('useremail')
    user      = User.all().filter('email =', email).get()
    
    if not user:
      self.set_error(u'El correo ingresado no corresponde a ningún usuario.')
      return self.redirect_to('backend/auth/login')    
    
    # Mando Correo de restauración de contraseña.
    # Armo el contexto dado que lo utilizo para mail plano y mail HTML.
    context = { 'server_url':       'http://'+self.request.headers.get('host', 'no host')
              , 'user_name':        user.full_name
              , 'user_email':       user.email
              , 'realestate_name':  user.realestate.name
              , 'restore_link':     self.url_for('backend/auth/restore', key=str(user.key()), _full=True) 
              , 'unrestore_link':   self.url_for('backend/auth/unrestore', key=str(user.key()), _full=True) 
              , 'support_url' :       'http://'+self.request.headers.get('host', 'no host')}
    
    # Armo el body en plain text.
    body = self.render_template('email/'+self.config['ultraprop']['mail']['password']['template']+'.txt', **context)  
    # Armo el body en HTML.
    html = self.render_template('email/'+self.config['ultraprop']['mail']['password']['template']+'.html', **context)  
    
    # Envío el correo.
    mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['password']['sender'], 
                 to=user.email,
                 subject="ULTRAPROP - Restauración de contraseña",
                 body=body,
                 html=html
                 )
    
    user.restore_password = 1             
    user.enabled          = 0
    user.save()
    
    self.set_ok(u'Un correo ha sido enviado a su casilla de email. Modifique su contraseña ingresando a ULTRAPROP a través de link recibido.<br/> Si no encuentra el correo en INBOX, búsquelo en SPAM.')
    return self.redirect_to('backend/auth/login')    