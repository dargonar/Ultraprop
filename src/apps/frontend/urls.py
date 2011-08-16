# -*- coding: utf-8 -*-
from webapp2 import Route, RedirectHandler
from webapp2_extras.routes import PathPrefixRoute

def get_rules():
    """Returns a list of URL rules for the Hello, World! application.

    
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
      # Esta la pongo aca por puta
      Route('/run/mapper',            name='run/mapper',          handler='apps.backend.property.RunMapper'),
      Route('/webclient/index.asp',   name='oldredir',            handler='apps.realestate.handlers.Redirect'),
      Route('/manda_bienvenida',      name='mandabien',           handler='apps.realestate.handlers.LaunchEmail'),
      # HACK: Urls de old ultraprop.
      Route('/Integrantes.asp',       name='redir/frontend/home', handler='apps.frontend.home.IndexRedir'),
      Route('/institucional.html',    name='redir/frontend/home', handler='apps.frontend.home.IndexRedir'),
      Route('/Contactenos.html',      name='redir/frontend/home', handler='apps.frontend.home.IndexRedir'),
      Route('/Centro.asp',            name='redir/frontend/home', handler='apps.frontend.home.IndexRedir'),
      
      Route('/',                                                    name='frontend/home',             handler='apps.frontend.home.Index'),
      
      Route('/mapa',                                                name='frontend/map',              handler='apps.frontend.map.Index'),
      
      Route('/mapa/<realestate>',                                   name='frontend/map/realestate',   handler='apps.frontend.map.Index:realesate_filtered'),
      
      Route('/link/copy',                                           name='frontend/link/copy',        handler='apps.frontend.link.ShortenLink'),
      Route('/link/copy/sendmail',                                  name='frontend/link/sendmail',    handler='apps.frontend.link.EmailShortenedLink'),
      Route('/link/share/',                                         name='frontend/link/share',       handler='apps.frontend.link.SearchShare'),
      Route('/link/map/<bitly_hash>',                               name='frontend/link/map',         handler='apps.frontend.link.LoadSearchLink'),
      
      Route('/service/search',                                      name='frontend/search',           handler='apps.frontend.search.Search'),
      
      Route('/compare',                                             name='compare',                   handler='apps.frontend.property_info.Compare'),
      Route('/service/popup/<key>/<bubble_css>/<oper>',             name='frontend/property_popup',   handler='apps.frontend.property_info.PopUp'),
      Route('/service/ficha/<key>/<oper>',                          name='frontend/property_ficha',   handler='apps.frontend.property_info.Ficha'),
      Route('/service/ficha/email/<key>/<oper>',                    name='frontend/ficha/sendemail',  handler='apps.frontend.property_info.SendMail'),
      Route('/email_task',                                          name='frontend/email_task',       handler='apps.frontend.email.SendTask'),
      #A borrar estos!!!!
      #Route('/ver/user/email/<key>/<realestate_key>/<oper>',        name='frontend/ver/useremail',    handler='apps.frontend.property_info.VerUserMail'),
      #Route('/ver/agent/email/<key>/<realestate_key>/<oper>',       name='frontend/ver/agentemail',   handler='apps.frontend.property_info.VerAgentMail'),
    ]
    
    return rules
