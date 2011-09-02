# -*- coding: utf-8 -*-
"""
    account handlers
    ~~~~~~~~
"""
import logging

from google.appengine.ext import db

from models import Invoice, RealEstate
from utils import need_auth, BackendHandler 

class Status(BackendHandler):
  @need_auth()
  def get(self, **kwargs):
    re          = db.get(self.get_realestate_key())
    invoices    = Invoice.all().filter('realestate', re.key()).filter('state', Invoice._NOT_PAID)
    total_debt  = reduce(lambda x,i: x+i.amount, invoices, 0)*1.21
    mnutop      = 'cuenta'
    
    #flash = None
    #if re.status == RealEstate._TRIAL or re.status == RealEstate._TRIAL_END:
    #  flash = self.build_info('Para continuar luego del periodo de prueba debe abonar la factura que aparece debajo.')

    params = {
      're'        :re,
      'invoices'  :invoices,
      'total_debt':total_debt,
      'mnutop'    :mnutop,
      'plan'      :re.plan,
    }
      
    return self.render_response('backend/account.html', **params)