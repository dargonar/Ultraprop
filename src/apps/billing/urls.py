# -*- coding: utf-8 -*-
from webapp2 import Route
from webapp2_extras.routes import PathPrefixRoute


def get_rules():
    """Returns a list of URL rules for the Hello, World! application.

    .param app.
        The WSGI application instance.
    .return.
        A list of class.`tipfy.Rule` instances.
    """
    rules = [
      PathPrefixRoute('/billing', [NamePrefixRoute('billing/', [
          
        PathPrefixRoute('/payment', [
          Route('/download'              , name='payment/download'       , handler='apps.billing.payment.Download'),
          Route('/assing'                , name='payment/assing'         , handler='apps.billing.payment.Assing'),
        ]),
        
      ])])
    ]

    return rules
