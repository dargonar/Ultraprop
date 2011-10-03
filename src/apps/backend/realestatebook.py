# -*- coding: utf-8 -*-
"""
    Auth & RealState
    ~~~~~~~~
"""
from __future__ import with_statement

import logging
import re
from datetime import datetime
from google.appengine.ext import db, deferred
from google.appengine.api import mail

from utils import get_or_404, need_auth, BackendHandler, NetworkPropertyMapper
from models import RealEstate, RealEstateFriendship, Property

    
class Index(BackendHandler):
  @need_auth()
  def get(self, **kwargs):
    return self.redirect_to('backend/realestatebook/friends')
  

  #q = RealEstate.all().filter('name >= ', 'D').filter('name < ', 'd'+u'\ufffd').fetch(10)
  
class FriendRequest(BackendHandler):
  @need_auth()
  def post(self, **kwargs):
    
    realestate                    = get_or_404(self.get_realestate_key())
    friend_keys                   = self.request.POST['selected_friend_keys'].strip()
    if not friend_keys:
      self.set_warning(u'Seleccione al menos una inmobiliria.')
      return self.redirect_to('backend/realestatebook/friend_request')
    
    
    
    for rs_key in friend_keys.split(','):
      if not rs_key or len(rs_key)<1:
        continue
      req = RealEstateFriendship.all().filter('realestates = ', self.get_realestate_key()).filter('realestates = ', rs_key).get()
      if req:
        req.delete()
      
      realestate_b = db.get(rs_key)
      req = RealEstateFriendship.new_for_request(realestate, realestate_b)
      req.put()
      
      context = {'rs_requestor':           realestate, 
                 'rs_receiver':            realestate_b}
      body = self.render_template('email/realestate_friend_request.txt', **context)  
      # Armo el body en HTML.
      html = self.render_template('email/realestate_friend_request.html', **context)  
      
      # Envío el correo.
      mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['share_link']['sender'], 
                   to=realestate_b.email,
                   subject="ULTRAPROP - Pedido de amistad",
                   body=body,
                   html=html)
      
      body = self.render_template('email/realestate_friend_request_cc.txt', **context)  
      # Armo el body en HTML.
      html = self.render_template('email/realestate_friend_request_cc.html', **context)  
      
      mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['share_link']['sender'], 
                   to=realestate.email,
                   subject="ULTRAPROP - Pedido de amistad",
                   body=body,
                   html=html
                 )
      
    self.set_ok(u'Su pedido de amistad fue enviado con éxito.')
    
    return self.redirect_to('backend/realestatebook/friend_request')
  
  @need_auth()
  def get(self, **kwargs):
    kwargs['mnutop']              = 'realestatebook'
    realestate                    = get_or_404(self.get_realestate_key())
    keys = [realestate.key()]
    
    friends       = RealEstateFriendship.all(keys_only=True).filter('realestates = ', str(realestate.key())).filter('state = ', RealEstateFriendship._ACCEPTED).fetch(1000)
    requesteds    = RealEstateFriendship.all(keys_only=True).filter('realestates = ', str(realestate.key())).fetch(1000)
    
    realestate_str_key = str(realestate.key())
    query = RealEstate.all().filter('__key__ != ', realestate.key())
    if not self.has_role('ultraadmin'):
      query.filter(' is_tester = ', False)
    
    already_friends   = []
    if friends:
      for request in friends:
        current_key = RealEstateFriendship.get_the_other(request, realestate_str_key, get_key=False)
        already_friends.append(current_key)
    
    denied            = []
    friend_req_sent   = []
    if requesteds:
      for request in requesteds:
        current_key = RealEstateFriendship.get_the_other(request, realestate_str_key, get_key=False)
        if current_key not in already_friends:
          if RealEstateFriendship.is_sender_ex(request, realestate_str_key):
            friend_req_sent.append(current_key)
          else:
            if db.get(request).state==RealEstateFriendship._DENIED:
              denied.append(current_key)
            else:
              friend_req_sent.append(current_key)
              
    kwargs['denied']                  = denied
    kwargs['already_friends']         = already_friends
    kwargs['friend_req_sent']         = friend_req_sent
    kwargs['realestates']             = query.fetch(1000)
    return self.render_response('backend/realestatebook_search.html', **kwargs)
  
  @need_auth()
  def reject(self, **kwargs):
    return self.accept_or_reject(False, **kwargs)
      
  @need_auth()
  def accept(self, **kwargs):
    return self.accept_or_reject(True, **kwargs)
  
  def accept_or_reject(self, accept=True, **kwargs):
    realestate                    = get_or_404(self.get_realestate_key())
    req                           = get_or_404(kwargs.get('key'))
    if req.is_sender(realestate):
      self.abort(500)
    
    my_key        = self.get_realestate_key()
    realestate_b  = req.get_the_other_realestate(my_key, key_only=False)
    context       = { 'rs_requestor':           realestate_b, 
                      'rs_receiver':          realestate}

    if accept:
      req.accept()
      owner   = req.get_the_other_realestate(my_key, key_only=True)
      tmp     = NetworkPropertyMapper(owner, my_key, do_add=True, for_admin=True, for_website=False)
      deferred.defer(tmp.run)
      
      tmp2    = NetworkPropertyMapper(my_key, owner, do_add=True, for_admin=True, for_website=False)
      deferred.defer(tmp2.run)
      
      body = self.render_template('email/realestate_friend_accepted.txt', **context)  
      html = self.render_template('email/realestate_friend_accepted.html', **context)  
      
      # Envío el correo.
      mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['share_link']['sender'], 
                 to=realestate_b.email,
                 subject="ULTRAPROP - Pedido de amistad",
                 body=body,
                 html=html)
    
    
      self.set_ok('La solicitud de amistad ha sido aceptada.')
    else:
      # body = self.render_template('email/realestate_friend_denied.txt', **context)  
      # html = self.render_template('email/realestate_friend_denied.html', **context) 
      req.reject()
      self.set_ok('La solicitud de amistad ha sido rechazada.')
      
    return self.redirect_to('backend/realestatebook/requests')

class Requests(BackendHandler):
  _SENT     = 1
  _RECEIVED = 2
  
  @need_auth()
  def get(self, **kwargs):
    kwargs['filter']            = int(self.request.GET.get('filter', self._RECEIVED))
    return self.get2(**kwargs)
    
  @need_auth()
  def post(self, **kwargs):
    kwargs['filter']            = int(self.request.POST.get('filter', self._RECEIVED))
    return self.get2(**kwargs)
    
  def get2(self, **kwargs):
    realestate                    = get_or_404(self.get_realestate_key())
    kwargs['realestate']          = realestate
    kwargs['mnutop']              = 'realestatebook'
    
    # if 'filter' not in kwargs or kwargs['filter']==0:
      # kwargs['requests']            = RealEstateFriendship.all().filter('realestates = ', str(realestate.key())).filter('state ', RealEstateFriendship._REQUESTED).fetch(1000)
      # kwargs['filter']              = 0
    # else:
    if kwargs['filter'] == self._SENT:
      kwargs['requests']            = RealEstateFriendship.all().filter('realestate_a = ', realestate.key()).filter('state in ', [RealEstateFriendship._REQUESTED, RealEstateFriendship._DENIED]).fetch(1000)
    else:
      kwargs['requests']            = RealEstateFriendship.all().filter('realestate_b = ', realestate.key()).filter('state = ', RealEstateFriendship._REQUESTED).fetch(1000)
    
    kwargs['_SENT']       = self._SENT
    kwargs['_RECEIVED']   = self._RECEIVED
    return self.render_response('backend/realestatebook_requests.html', **kwargs)
    
class Friends(BackendHandler):
  @need_auth()
  def get(self, **kwargs):
    realestate                    = get_or_404(self.get_realestate_key())
    kwargs['realestate']          = realestate
    kwargs['mnutop']              = 'realestatebook'
    kwargs['requests']            = RealEstateFriendship.all().filter('realestates = ', str(realestate.key())).filter('state = ', RealEstateFriendship._ACCEPTED).fetch(1000)
    
    return self.render_response('backend/realestatebook_friends.html', **kwargs)
  
  @need_auth()
  def delete(self, **kwargs):
    realestate                    = get_or_404(self.get_realestate_key())
    req                           = get_or_404(kwargs.get('key'))
    if str(realestate.key()) not in req.realestates:
      self.abort(500)
    my_key  = self.get_realestate_key()
    owner   = req.get_the_other_realestate(my_key, key_only=True)
    tmp     = NetworkPropertyMapper(owner, my_key, do_add=False, for_admin=True, for_website=True)
    deferred.defer(tmp.run)
    tmp2    = NetworkPropertyMapper(my_key, owner, do_add=False, for_admin=True, for_website=True)
    deferred.defer(tmp2.run)
    
    #Envío el correo.
    realestate_b = db.get(owner)
    context = {'rs':           realestate, 
               'rs_other':     realestate_b}
    body = self.render_template('email/realestate_friend_deleted.txt', **context)  
    html = self.render_template('email/realestate_friend_deleted.html', **context)  
    mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['share_link']['sender'], 
                 to=realestate_b.email,
                 subject=u"ULTRAPROP - Finalización de amistad",
                 body=body,
                 html=html)
    
    req.delete()
    
    self.set_ok('Su Red ha sido actualizada satisfactoriamente.')
    return self.redirect_to('backend/realestatebook/friends')
  
  @need_auth()
  def share(self, **kwargs):
    realestate                    = get_or_404(self.get_realestate_key())
    req                           = get_or_404(kwargs.get('key'))
    if str(realestate.key()) not in req.realestates:
      self.abort(500)
    if req.is_sender(realestate):
      req.rs_a_shows_b     = True
    else:
      req.rs_b_shows_a     = True
    req.save()
    
    my_key  = self.get_realestate_key()
    owner   = req.get_the_other_realestate(my_key, key_only=True)
    tmp     = NetworkPropertyMapper(owner, my_key, do_add=True, for_admin=False, for_website=True)
    deferred.defer(tmp.run)
    
    realestate_b = req.get_the_other_realestate(my_key, key_only=False)
    context = {'rs':                    realestate, 
               'rs_other':              realestate_b,
               'rs_other_not_sharing':  req.is_the_other_realestate_offering_my_props(my_key)}
    body = self.render_template('email/realestate_friend_is_sharing.txt', **context)  
    html = self.render_template('email/realestate_friend_is_sharing.html', **context)  
    
    # Envío el correo.
    mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['share_link']['sender'], 
                 to=realestate_b.email,
                 subject=u"ULTRAPROP - Red ULTRAPROP",
                 body=body,
                 html=html)
    
    self.set_ok('La amistad ha sido actualizada.')
    return self.redirect_to('backend/realestatebook/friends')
    
  @need_auth()
  def unshare(self, **kwargs):
    realestate                    = get_or_404(self.get_realestate_key())
    req                           = get_or_404(kwargs.get('key'))
    if str(realestate.key()) not in req.realestates:
      self.abort(500)
    if req.is_sender(realestate):
      req.rs_a_shows_b     = False
    else:
      req.rs_b_shows_a     = False
    req.save()
    
    my_key  = self.get_realestate_key()
    owner   = req.get_the_other_realestate(my_key, key_only=True)
    tmp     = NetworkPropertyMapper(owner, my_key, do_add=False, for_admin=False, for_website=False)
    deferred.defer(tmp.run)
    
    realestate_b = req.get_the_other_realestate(my_key, key_only=False)
    context = {'rs':           realestate, 
               'rs_other':     realestate_b}
    body = self.render_template('email/realestate_friend_stopped_sharing.txt', **context)  
    html = self.render_template('email/realestate_friend_stopped_sharing.html', **context)  
    
    # Envío el correo.
    mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['share_link']['sender'], 
                 to=realestate_b.email,
                 subject=u"ULTRAPROP - Finalización de amistad",
                 body=body,
                 html=html)
                 
    self.set_ok('La amistad ha sido actualizada.')
    return self.redirect_to('backend/realestatebook/friends')