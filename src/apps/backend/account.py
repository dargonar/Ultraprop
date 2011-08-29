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
    realestate = db.get(self.get_realestate_key())
    invoices = Invoice.all().filter('realestate', realestate.key()).filter('state', Invoice._NOT_PAID)
    mnutop   = 'cuenta'

    flash = None
    if realestate.status == RealEstate._TRIAL or realestate.status == RealEstate._TRIAL_END:
      flash = self.build_info('Para continuar luego del periodo de prueba debe abonar la factura que aparece debajo.')
    
    return self.render_response('backend/account.html', invoices=invoices, flash=flash, realestate=realestate, plan=realestate.plan, mnutop=mnutop)