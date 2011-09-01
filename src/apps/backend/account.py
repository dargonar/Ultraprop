# -*- coding: utf-8 -*-
"""
    account handlers
    ~~~~~~~~
"""
import logging

from google.appengine.ext import db

from models import Invoice, RealEstate
from utils import need_auth, BackendHandler 

class PaymentCancel(BackendHandler):
  @need_auth()
  def get(self, **kwargs):
    self.set_info('El pago fue cancelado')
    self.redirect_to('backend/account/status')

class PaymentDone(BackendHandler):
  @need_auth()
  def get(self, **kwargs):
    self.set_ok('El pago fue realizado con exito')
    self.redirect_to('backend/account/status')

class PaymentPending(BackendHandler):
  @need_auth()
  def get(self, **kwargs):
    self.set_ok('Usted eligio un medio de pago en efectivo, la factura quedara en estado pendiente hasta que se acredite el pago. Muchas Gracias.')
    self.redirect_to('backend/account/status')

class Status(BackendHandler):
  @need_auth()
  def get(self, **kwargs):
    re          = db.get(self.get_realestate_key())
    invoices    = Invoice.all().filter('realestate', re.key()).filter('state', Invoice._NOT_PAID)
    total_debt  = reduce(lambda x,i: x+i.amount, invoices, 0)*1.21
    mnutop      = 'cuenta'
    error_url   = self.url_for('backend/account/payment-cancel', _full=True)
    ok_url      = self.url_for('backend/account/payment-done', _full=True)
    pending_url = self.url_for('backend/account/payment-pending', _full=True)
    
    #flash = None
    #if re.status == RealEstate._TRIAL or re.status == RealEstate._TRIAL_END:
    #  flash = self.build_info('Para continuar luego del periodo de prueba debe abonar la factura que aparece debajo.')

    params = {
      're'        :re,
      'invoices'  :invoices,
      'total_debt':total_debt,
      'mnutop'    :mnutop,
      'error_url' :error_url,
      'ok_url'    :ok_url,
      'pending_url':pending_url,
      'plan'      :re.plan,
    }
      
    return self.render_response('backend/account.html', **params)