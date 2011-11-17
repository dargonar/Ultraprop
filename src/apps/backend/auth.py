# -*- coding: utf-8 -*-
"""
    Auth & RealState
    ~~~~~~~~
"""
import logging
from datetime import datetime, date, timedelta
from google.appengine.api import mail

from webapp2 import cached_property
from backend_forms import SignUpForm, validate_domain_id
from models import RealEstate, User, Plan, Invoice
from utils import get_or_404, BackendHandler
from myfilters import do_slugify

class Index(BackendHandler):
  def get(self, **kwargs):
    if self.is_logged and self.is_enabled:
      if self.session['account.realestate.status'] == RealEstate._NO_PAYMENT:
        return self.redirect_to('backend/account/status')
      else:
        return self.redirect_to('property/list')
    
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
    
    # TODO: PENSAR -> status es para mantener el estado de pagos.
    # deberiamos tener otra bandera para indicar si la informacion del realestate esta completa
    
    if user.realestate.status == RealEstate._NO_PAYMENT:
      return self.redirect_to('backend/account/status')
    
    #if not self.is_realestate_enabled:
    #  self.set_info('Debe configurar la inmobiliaria para comenzar a operar.')
    #  return self.redirect_to('backend/realestate/edit')
    
    return self.redirect_to('property/list')
    
class Logout(BackendHandler):
  def get(self, **kwargs):
    self.session.clear()  
    return self.redirect_to('backend/auth/login')
    
class SignUp(BackendHandler):
  promo = 'promo-3-meses'
  #Edit/New
  def get(self, **kwargs):
    
    if self.is_logged:
      return self.redirect_to('property/list')
    
    kwargs['form']   = self.form
    if 'promo' in kwargs and kwargs.get('promo')==self.promo:
      # ...el de la promo
      kwargs['promo'] = self.promo
      plan  = Plan.all().filter('name','promo-3-meses').get()
      if not plan:
        p = Plan()
        p.name = 'promo-3-meses'
        p.description = u'Campaña lanzamiento $79'
        p.type = Plan._MONTHLY
        p.amount = 79
        p.free_days = 90
        p.save()
        plan = p
      kwargs['plan'] = plan
    else:
      # ...o plan por defecto
      kwargs['plan'] = Plan.all().filter('name','promo-lanzamiento').get()
      kwargs['promo'] = None
    
    return self.render_response('backend/signup.html', **kwargs)
  
  #Create/Save RealEstate & User.
  def post(self, **kwargs):
    self.request.charset  = 'utf-8'
    
    plan = None
    # Aca traemos el plan...
    if 'promo' in kwargs and kwargs.get('promo')==self.promo:
      # ...el de la promo
      plan = Plan.all().filter('name','promo-3-meses').get()
      if not plan:
        p = Plan()
        p.name = 'promo-3-meses'
        p.description = u'Campaña lanzamiento $79'
        p.type = Plan._MONTHLY
        p.amount = 79
        p.free_days = 90
        p.save()
        plan = p
    else:
      # ...o plan por defecto
      plan = Plan.all().filter('name','promo-lanzamiento').get()
      
    form_validated = self.form.validate()
    if not form_validated:
      kwargs['form']         = self.form
      if self.form.errors:
        kwargs['flash']      = self.build_error('Verifique los datos ingresados:')# + '<br/>'.join(reduce(lambda x, y: str(x)+' '+str(y), t) for t in self.user_form.errors.values()))
      kwargs['plan']         = plan
      return self.render_response('backend/signup.html', **kwargs)
    
    # Generamos la inmo en estado TRIAL y le ponemos el Plan
    realEstate = RealEstate.new()
    realEstate.telephone_number = self.form.telephone_number.data
    realEstate.name             = self.form.name.data
    realEstate.email            = self.form.email.data
    realEstate.plan             = plan
    realEstate.status           = RealEstate._REGISTERED
    
    # Ya tenemos registrado ese domain_id
    realEstate.domain_id = do_slugify(realEstate.name)
    tmp = validate_domain_id(realEstate.domain_id)
    if tmp['result'] != 'free':
      realEstate.domain_id = realEstate.domain_id + datetime.now().strftime('%Y%m%d%H%M')
    
    realEstate.put()
    
    # Generamos la primer factura con fecha hoy+dias_gratis
    # Utilizamos el indicador I para indicar 'id' en vez de 'name'
    first_date = (datetime.utcnow() + timedelta(days=plan.free_days)).date()
    if first_date.day > 28:
      first_date = date(first_date.year, first_date.month, 28)
    
    invoice = Invoice()
    invoice.realestate = realEstate
    invoice.trx_id     = '%sI%d' % ( first_date.strftime('%Y%m'), realEstate.key().id() )
    invoice.amount     = plan.amount
    invoice.state      = Invoice._NOT_PAID
    invoice.date       = first_date
    invoice.put()
    
    # Volvemos a guardar el realEstate con los datos nuevos
    realEstate.last_invoice = invoice.date
    realEstate.save()

    # Generamos el usuario y le asignamos la realestate
    user = User.new()
    user.email            = self.form.email.data
    user.password         = self.form.password.data
    user.rol              = 'owner'
    user.realestate       = realEstate
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
    
    if user.enabled:
      return self.redirect_to('backend/auth/login')
    
    user.enabled = 1
    user.save()
    
    re = user.realestate
    # NOTE: Ja! me querias cagar!!??? clickeaste el link del mail cuando estabas en no_payment???
    # Ja! no te pongo ni en pedo en trial!!! ... mm creo que arriba ya se validaba
    if re.status == RealEstate._REGISTERED:
      re.status = RealEstate._TRIAL
    re.enable=1
    re.save()
    
    self.do_login(user)
    
    self.set_ok('Su correo ha sido validado. Por favor complete la información de la inmobiliaria para comenzar a operar con ULTRAPROP.')
    
    return self.redirect_to('property/list')

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
    
    self.set_ok(u'Un correo ha sido enviado a su casilla de email.<br/> Si no encuentra el correo en INBOX, búsquelo en SPAM.')
    return self.redirect_to('backend/auth/login')    