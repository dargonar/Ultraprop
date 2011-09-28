# -*- coding: utf-8 -*-
"""
    Auth & RealState
    ~~~~~~~~
"""
from __future__ import with_statement

import logging
import re

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
      realestate_b = db.get(rs_key)
      req = RealEstateFriendship.new_for_request(realestate, realestate_b)
      # req.realestate_a = realestate
      # req.realestate_b = realestate_b
      req.put()
      # mail_to=realestate_b.email
      # body='La inmobiliaria %s desea ser su amiga.' %  (realestate.name)
      # mail.send_mail(sender="www.ultraprop.com.ar <info@ultraprop.com.ar>", 
                   # to       = mail_to,
                   # subject  = "ULTRAPROP: Una inmobiliaria quiere ser su amiga",
                   # body     = body)
    
    self.set_ok(u'Su pedido de amistad fue enviado con éxito.')
    
    return self.redirect_to('backend/realestatebook/friend_request')
  
  @need_auth()
  def get(self, **kwargs):
    kwargs['mnutop']              = 'realestatebook'
    realestate                    = get_or_404(self.get_realestate_key())
    keys = [realestate.key()]
    
    requests                      = RealEstateFriendship.all(keys_only=True).filter('realestates = ', str(realestate.key())).fetch(1000)
    #.filter('state = ', RealEstateFriendship._REQUESTED)
    
    realestate_str_key = str(realestate.key())
    query = RealEstate.all().filter('__key__ != ', realestate.key())
    
    if requests:
      for request in requests:
        current_key = RealEstateFriendship.get_the_other(request, realestate_str_key, get_key=True)
        query.filter('__key__ != ', current_key)
        
    kwargs['realestates']         = query.fetch(1000)
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
    if accept:
      req.accept()
      
      my_key  = self.get_realestate_key()
      owner   = req.get_the_other_realestate(my_key, key_only=True)
      tmp     = NetworkPropertyMapper(owner, my_key, do_add=True, field=Property._RS_FRIEND_FIELD)
      deferred.defer(tmp.run)
      
      tmp2    = NetworkPropertyMapper(my_key, owner, do_add=True, field=Property._RS_FRIEND_FIELD)
      deferred.defer(tmp2.run)
      
      self.set_ok('La solicitud de amistad ha sido aceptada.')
    else:
      req.delete()
      self.set_ok('La solicitud de amistad ha sido rechazada.')
    return self.redirect_to('backend/realestatebook/requests')

class Requests(BackendHandler):
  _SENT     = 1
  _RECEIVED = 2
  
  @need_auth()
  def get(self, **kwargs):
    kwargs['filter']            = int(self.request.GET.get('filter', 0))
    return self.get2(**kwargs)
    
  @need_auth()
  def post(self, **kwargs):
    kwargs['filter']            = int(self.request.POST.get('filter', 0))
    return self.get2(**kwargs)
    
  def get2(self, **kwargs):
    realestate                    = get_or_404(self.get_realestate_key())
    kwargs['realestate']          = realestate
    kwargs['mnutop']              = 'realestatebook'
    
    if 'filter' not in kwargs:
      kwargs['requests']            = RealEstateFriendship.all().filter('realestates = ', str(realestate.key())).filter('state = ', RealEstateFriendship._REQUESTED).fetch(1000)
      kwargs['filter']              = 0
    else:
      if kwargs['filter'] == self._SENT:
        kwargs['requests']            = RealEstateFriendship.all().filter('realestate_a = ', realestate.key()).filter('state = ', RealEstateFriendship._REQUESTED).fetch(1000)
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
    tmp     = NetworkPropertyMapper(owner, my_key, do_add=False, field=Property._RS_FRIEND_FIELD, field2=Property._RS_SHARE_FIELD)
    deferred.defer(tmp.run)
    tmp2    = NetworkPropertyMapper(my_key, owner, do_add=False, field=Property._RS_FRIEND_FIELD, field2=Property._RS_SHARE_FIELD)
    deferred.defer(tmp2.run)
    
    req.delete()
    self.set_ok('La amistad ha sido dada de baja.')
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
    tmp     = NetworkPropertyMapper(owner, my_key, do_add=True, field=Property._RS_SHARE_FIELD)
    deferred.defer(tmp.run)

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
    tmp     = NetworkPropertyMapper(owner, my_key, do_add=False, field=Property._RS_SHARE_FIELD)
    deferred.defer(tmp.run)
    
    self.set_ok('La amistad ha sido actualizada.')
    return self.redirect_to('backend/realestatebook/friends')