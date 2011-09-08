# -*- coding: utf-8 -*-
"""
    Payment module
    ~~~~~~~~
"""
import logging
import urllib2
import urllib

IPN_URL     = 'http://argentina.dineromail.com/vender/ConsultaPago.asp'
#IPN_URL     = 'http://localhost:8080/img/ipn.xml'
IPN_PARAMS  = {'Email'    :'ptutino@gmail.com',
               'Acount'   :'22676371',
               'Pin'      :'50XBXYROC5',
               'XML'      :'1'}

def ipn_download(date_from, date_to):
  IPN_PARAMS['StartDate'] = date_from.strftime('%Y%m%d')
  IPN_PARAMS['EndDate'  ] = date_to.strftime('%Y%m%d')

  url    = IPN_URL + '?' + urllib.urlencode(IPN_PARAMS)
  logging.info('Voy a pedir %s' % url)
  
  result = urllib2.urlopen(url).read()
  return result
