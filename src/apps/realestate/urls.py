# -*- coding: utf-8 -*-
from webapp2 import Route
from webapp2_extras.routes import PathPrefixRoute


def get_rules():
    """Returns a list of URL rules for the Hello, World! application.

    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
      PathPrefixRoute('/www', [
          Route('/<realestate>/',                     name='realestate/home',           handler='apps.realestate.handlers.Index'),
          Route('/<realestate>',                      name='realestate/home',           handler='apps.realestate.handlers.Index'),
          Route('/<realestate>/busqueda',             name='realestate/search',         handler='apps.realestate.search.Search'),
          Route('/<realestate>/busqueda/<page>',      name='realestate/search/page',    handler='apps.realestate.search.Search'),
          Route('/<realestate>/ficha/<key>/<oper>',   name='realestate/ficha',          handler='apps.realestate.ficha.Show'),
          Route('/<realestate>/info',                 name='realestate/info',           handler='apps.realestate.handlers.Info'),
        ]),
      # RealEstate Home por slug
      Route('/<realestate_slug>',                     name='realestate/search_slug',    handler='apps.realestate.handlers.Index:by_slug'),
      Route('/<realestate>/theme_preview/<theme>',    name='realestate/theme_preview',  handler='apps.realestate.handlers.Index:theme_preview'),
      Route('/<realestate>/texts_preview/<title>/<message>',    name='realestate/texts_preview',  handler='apps.realestate.handlers.Index:texts_preview'),
        
    ]

    return rules
