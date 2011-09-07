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
  'template_path': 'templates',
  'compiled_path': 'templates_compiled',
  'force_compiled': False,

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
    
    'trial_will_expire':  {'sender':'info@ultraprop.com.ar', 'template':'trial_will_expire'},
    'trial_ended':        {'sender':'info@ultraprop.com.ar', 'template':'trial_ended'},
    'no_payment':         {'sender':'info@ultraprop.com.ar', 'template':'no_payment'},
    'enabled_again':      {'sender':'info@ultraprop.com.ar', 'template':'enabled_again'},
    'payment_received':   {'sender':'info@ultraprop.com.ar', 'template':'payment_received'},
    'new_invoice':        {'sender':'info@ultraprop.com.ar', 'template':'new_invoice'},
    'pending_invoices':   {'sender':'info@ultraprop.com.ar', 'template':'pending_invoices'},

    'reply_consultas':    {'mail':'consultas@ultraprop.com.ar'},

  },
  'recaptcha':{
    'public_key':	'6LdX18YSAAAAAIVJsoxIG9AxOOUb2WExYDDjqr5z',
    'private_key':	'6LdX18YSAAAAADcIPHyzim5Lx7pTQtz5e_bLUswC'
  }
}