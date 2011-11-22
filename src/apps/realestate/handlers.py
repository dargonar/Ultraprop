# -*- coding: utf-8 -*-
import logging

from google.appengine.ext import db
from google.appengine.api import taskqueue
from google.appengine.api.images import get_serving_url

from webapp2 import cached_property, abort

from models import Property
from backend_forms import PropertyFilterForm, PropertyContactForm
from utils import get_or_404, RealestateHandler
from search_helper_func import PropertyPaginatorMixin
# Mail de bienvenida
from google.appengine.api import mail
from models import User, RealEstate
from theme_manager import default_theme, themes, get_props_at_home

# Index va a ser la homepage de la inmobiliaria, creo que quedará obsoleto.    
class Index(RealestateHandler, PropertyPaginatorMixin):
  realestate = None
  
  def get(self, **kwargs):
    self.realestate = get_or_404(self.get_realestate_key_ex(kwargs.get('realestate')))
    return self.getto(realestate=self.realestate)
  
  def by_slug(self, **kwargs):
    self.realestate = RealEstate.all().filter(' domain_id = ', kwargs.get('realestate_slug')).get()
    if not self.realestate:
      abort(404)
    return self.getto(realestate=self.realestate, **kwargs)
  
  def getto(self, realestate, **kwargs):
    # Ponemos la pantalla de disabled si esta en NO_PAYMENT
    if realestate.status == RealEstate._NO_PAYMENT:
      return self.render_response('realestate/disabled.html', realestate=realestate)
      
    kwargs['realestate']        = realestate
    kwargs['menu_item']         = 'index'
    kwargs['form']              = self.form
    
    kwargs['properties']        = Property.all().filter(' location_geocells = ', RealEstate.get_realestate_sharing_key(None, realestate=realestate)).filter(' status = ', Property._PUBLISHED).fetch(get_props_at_home(realestate.get_web_theme()))  
      
    return self.render_response('realestate/index.html', **kwargs)
  
  def theme_preview(self, **kwargs):
    self.realestate = get_or_404(self.get_realestate_key_ex(kwargs.get('realestate')))
    if not self.realestate:
      abort(404)
    del(kwargs['realestate'])
    
    if 'theme' in kwargs and kwargs.get('theme') in themes.keys():
      #HACK!
      self.realestate.web_theme = kwargs.get('theme')
      
    return self.getto(realestate=self.realestate, **kwargs)
  
  def texts_preview(self, **kwargs):
    self.request.charset = 'utf-8'
    
    self.realestate = get_or_404(self.get_realestate_key_ex(kwargs.get('realestate')))
    if not self.realestate:
      abort(404)
    del(kwargs['realestate'])
    
    if 'title' in kwargs:
      #HACK!
      self.realestate.tpl_title = kwargs.get('title').decode('utf-8') 
    
    if 'message' in kwargs:
      #HACK!
      self.realestate.tpl_text = kwargs.get('message').decode('utf-8') 
      
    return self.getto(realestate=self.realestate, **kwargs)
    
# Info de la propiedad, creo que quedará obsoleto.    
class Info(RealestateHandler):
  def get(self, **kwargs):
    realestate = get_or_404(self.get_realestate_key_ex(kwargs.get('realestate')))
    
    # Ponemos la pantalla de disabled si esta en NO_PAYMENT
    if realestate.status == RealEstate._NO_PAYMENT:
      return self.render_response('realestate/disabled.html', realestate=realestate)
    
    kwargs['realestate']  = realestate
    kwargs['realestate_logo'] = realestate.logo_url
    kwargs['menu_item']   = 'info'
    kwargs['form']        =  self.form
    
    return self.render_response('realestate/contact.html', **kwargs)
  
  def post(self, **kwargs):
    self.request.charset = 'utf-8'
    realestate            = kwargs['realestate']
    
    # Ponemos la pantalla de disabled si esta en NO_PAYMENT
    re = get_or_404(self.get_realestate_key_ex(realestate))
    if re.status == RealEstate._NO_PAYMENT:
      return self.render_response('realestate/disabled.html', realestate=re)

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
      taskqueue.add(url=self.url_for('backend/email_task'), params=dict({'action':'contact_user'}, **context), transactional=True)
      taskqueue.add(url=self.url_for('backend/email_task'), params=dict({'action':'contact_agent'}, **context), transactional=True)
    
    db.run_in_transaction(txn)
    
    self.set_ok('Tu consulta enviada satisfactoriamente. Te hemos enviado una copia de la consulta a tu correo.')   
    return self.redirect_to('realestate/info', realestate=realestate)
    
  @cached_property
  def form(self):
    return PropertyContactForm(self.request.POST)