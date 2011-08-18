# -*- coding: utf-8 -*-
config = {}

config['webapp2'] = {
    'apps_installed': [
        'apps.backend',
        'apps.frontend',
        'apps.realestate',
    ],
}

config['webapp2_extras.sessions'] = {
  'secret_key'  : 'ultra daga de 26x6 reales',
  'cookie_name' : 'ultras',
}

config['webapp2_extras.jinja2'] = {
  'environment_args': {
    'autoescape': False,
  }
}

config['ultraprop'] = {
  'mail':{
    'signup':             {'sender':'info@ultraprop.com.ar', 'template':'welcome'},
    'password':           {'sender':'info@ultraprop.com.ar', 'template':'forgot_password'},
    'requestinfo_user':   {'sender':'info@ultraprop.com.ar', 'template':'request_info_to_user'},
    'requestinfo_agent':  {'sender':'info@ultraprop.com.ar', 'template':'request_info_to_agent'},
    'share_link':         {'sender':'info@ultraprop.com.ar', 'template':'share_link'},
    'contact_user':       {'sender':'info@ultraprop.com.ar', 'template':'contact_to_user'},
    'contact_agent':      {'sender':'info@ultraprop.com.ar', 'template':'contact_to_agent'},
    'reply_consultas':    {'mail':'consultas@ultraprop.com.ar'},

  },
  'recaptcha':{
    'public_key':	'6LdX18YSAAAAAIVJsoxIG9AxOOUb2WExYDDjqr5z',
    'private_key':	'6LdX18YSAAAAADcIPHyzim5Lx7pTQtz5e_bLUswC'
  }
}