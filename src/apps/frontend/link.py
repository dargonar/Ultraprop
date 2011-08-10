# -*- coding: utf-8 -*-
import logging
import urllib
import cgi

from webapp2 import cached_property, Response
from webapp2_extras.json import json, decode

from google.appengine.api import urlfetch
from google.appengine.api import mail

from search_helper import config_array, MAX_QUERY_RESULTS
from forms import EmailLinkForm
from utils import FrontendHandler, get_bitly_url

# Dummy Handler, por si chequea bit.ly.
class SearchShare(FrontendHandler):
  def get(self, **kwargs):
    return self.redirect_to('frontend/map')

class LoadSearchLink(FrontendHandler):
  def get(self, **kwargs):
    bitly_hash = kwargs.get('bitly_hash', '')
    if len(bitly_hash)<1:
      return redirect('frontend/map')
    
    url = 'http://bit.ly/' + bitly_hash
    expander_params =   { "login"    : "diventiservices",
                         "apiKey"   : "R_3a5d98588cb05423c22de21292cd98d6",
                         "shortUrl"  : url, 
                         "format"   : "json"
                         }

                         
    form_data = urllib.urlencode(expander_params)             
    
    post_url='http://api.bitly.com/v3/expand?'+form_data
    
    result = urlfetch.fetch(url=post_url,
                            method=urlfetch.GET)
    
    bitlydata = decode(result.content)

    if 'expand' not in bitlydata['data']:
      return redirect('frontend/map')
    if 'long_url' not in bitlydata['data']['expand'][0]:
      return redirect('frontend/map')
    
    long_url = bitlydata['data']['expand'][0]['long_url']
    
    query_string = long_url.split('?')[1]
    
    query_dict = cgi.parse_qs(query_string)
    
    south         = query_dict['south'][0]
    north         = query_dict['north'][0]
    west          = query_dict['west'][0]
    east          = query_dict['east'][0]
    center_lat    = (float(north) + float(south))/2
    center_lon    = (float(east) + float(west))/2
    
    dict = {}
    for key in query_dict.keys():
      value = query_dict[key][0]
      if value is not None and len(str(value))>0:
        dict[key] = value
    
    dict['center_lat'] = center_lat
    dict['center_lon'] = center_lon
    
    return self.render_response('frontend/index.html'
                          , config_arrayJSON=json.dumps(config_array)
                          , config_array=config_array
                          , max_results=MAX_QUERY_RESULTS
                          , preset=dict
                          , presetJSON=json.dumps(dict))

class EmailShortenedLink(FrontendHandler):
  def post(self, **kwargs):
    self.request.charset = 'utf-8'
    if self.form.validate():
    
      # ----------------    
      # Mando Correo para compartir link.
      context = {'link':                urllib.unquote(self.form.link.data), 
                 'email_to':            self.form.email.data
               , 'support_url' :        'http://'+self.request.headers.get('host', 'no host') 
               , 'server_url':                 'http://'+self.request.headers.get('host', 'no host')}
      # Armo el body en plain text.
      body = self.render_template('email/'+self.config['ultraprop']['mail']['share_link']['template']+'.txt', **context)  
      # Armo el body en HTML.
      html = self.render_template('email/'+self.config['ultraprop']['mail']['share_link']['template']+'.html', **context)  
      
      # Envío el correo.
      mail.send_mail(sender="www.ultraprop.com.ar <%s>" % self.config['ultraprop']['mail']['share_link']['sender'], 
                   to=context['email_to'],
                   subject="ULTRAPROP - Propiedades",
                   body=body,
                   html=html
                   )
      # ----------------
      
      self.response.write('Correo enviado satisfactoriamente.')
      return 
      
    # responsetxt = [reduce(lambda x, y: str(x)+' '+str(y), t) for t in self.form.errors.values()]
    responsetxt = 'Verifique los datos ingresados:' + '<br/>'.join(reduce(lambda x, y: str(x)+' '+str(y), t) for t in self.form.errors.values())
    self.response.status_int = 500
    self.response.write(responsetxt)
  
  @cached_property
  def form(self):
    return EmailLinkForm(self.request.POST)
    
class ShortenLink(FrontendHandler):
  def get(self, **kwargs):
    
    str_query     = self.request.query_string 
    str_query     += '&version=1' 
    
    link_url      = get_bitly_url(str_query)
    
    # Armo URL con 
    return self.render_json_response({ 'bitly':link_url })