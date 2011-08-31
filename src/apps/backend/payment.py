# -*- coding: utf-8 -*-
"""
    Payment module
    ~~~~~~~~
"""
import logging
from google.appengine.api import taskqueue

from datetime import datetime, timedelta
from xml.dom import minidom

from models import RealEstate, Payment, Invoice
from webapp2 import url_for, RequestHandler
from dm import ipn_download
from taskqueue import Mapper

class InvoicerMapper(Mapper):
  KIND    = RealEstate

  def send_mail(template, re):
    taskqueue.add(url=url_for('backend/email_task'), params={'template':template, 'rekey':str(re.key())})
    
  def map(self, re):
    
    if re.status == RealEstate._TRIAL:
      # Uso el 80% del free_days del Plan?
      delta = datetime.utcnow() - re.created_at
      if delta.days >= int(re.plan.free_days*0.80):
        re.state = RealEstate._TRIAL_END
        self.send_mail('trial_end', re)
      
    elif: re.state == RealEstate._TRIAL_END:
      # Llegamos a los free_days del Plan y todavia no pago?
      delta = datetime.utcnow() - re.created_at
      if delta.days >= re.plan.free_days:
        re.state = RealEstate._NO_PAYMENT
        self.send_mail('no_payment', re)
    
    elif: re.state == RealEstate._ENABLED:
      
      # Obtenemos el dia de ciclo
      cycle_day = re.created_at.day
      if cycle_day > 28:
        cycle_day = 28

      # Es el dia del ciclo?
      if datetime.utcnow().day == cycle_day:
        self.send_mail('new_invoice', re)
      
      
      delta = datetime.utcnow() - re.created_at
      if delta.days >= re.plan.free_days:
        re.state = RealEstate._NO_PAYMENT
        self.send_mail('no_payment', re)
    
    elif: re.state == RealEstate._NO_PAYMENT:
    
    return ([re], []) # update/delete
    

class PaymentAssingMapper(Mapper):
  KIND    = Payment
  FILTERS = [('assigned',0)]

  def map(self, payment):
    
    # Traemos la factura que este pago cancela el pago (payment)
    invoice = Invoice.all().filter('trx_id', payment.trx_id).get()
    if not invoice:
      logging.warning('No encontre factura para el pago %s' % str(payment.key()))
    else:
      # Ponemos la factura como pagada y dejamos asignado el pago
      invoice.state        = Invoice._PAID
      invoice.payment      = payment
      invoice.save()

    payment.assigned = 1
    return ([payment], []) # update/delete
  
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
    for pay in dom.getElementsByTagName('Credit'):
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