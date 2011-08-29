# -*- coding: utf-8 -*-
"""
    Payment module
    ~~~~~~~~
"""
import logging
from datetime import datetime, timedelta
from xml.dom import minidom

from models import Payment, Invoice
from webapp2 import RequestHandler
from dm import ipn_download
from taskqueue import Mapper

class PaymentAssingMapper(Mapper):
  KIND    = Payment
  FILTERS = [('assigned',0)]

  def map(self, entity):
    
    # Traemos la factura que este pago cancela el pago (entity)
    invoice = Invoice.all().filter('trx_id', entity.trx_id).get()
    if not invoice:
      logging.warning('No encontre factura para el pago %s' % str(entity.key()))
    else:
      # Ponemos la factura como pagada y dejamos asignado el pago
      invoice.state        = Invoice._PAID
      invoice.payment      = entity
      invoice.save()

    entity.assigned = 1
    return ([entity], []) # update/delete
  
# XML Helper
def get_xml_value(parent, name):
  firstChild = parent.getElementsByTagName(name)[0].firstChild
  return firstChild.nodeValue if firstChild else ''

class Download(RequestHandler):
  def post(self, **kwargs):
    self.request.charset  = 'utf-8'
    
    # Bajamos el xml con la api de IPN
    yesterday = datetime.utcnow() - timedelta(days=1)
    dom = minidom.parseString(ipn_download(yesterday, yesterday))
    
    # Verificamos que este todo bien el xml de vuelta
    state = int(get_xml_value(dom, 'State'))
    if state != 1:
      logging.error('Error al traer xml: %d' % state)
      self.response.write('ok')
      return

    # Parseamos y generamos los Payment
    to_save = []
    for pay in dom.getElementsByTagName('Pay'):
      p = Payment()
      p.invoice  = None
      p.date     = get_xml_value(pay,'Trx_Date')
      p.amount   = get_xml_value(pay,'Trx_Payment')
      p.assinged = 0
      
      to_save.append(p)
    
    # Salvamos todos los payments juntos
    db.put(to_save)
    
    # Mandamos a correr la tarea de mapeo
    defered.run(PaymentAssingMapper.run)
    self.response.write('ok')