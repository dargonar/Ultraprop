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
      Route('/tsk/email_task'           , name='backend/email_task'           , handler='apps.backend.email.SendTask'),
      Route('/tsk/run_ipn/<account>'    , name='billing/payment/download'     , handler='apps.backend.payment.Download'),
      Route('/tsk/run_invoicer'         , name='billing/payment/run_invoicer' , handler='apps.backend.payment.RunInvoicer'),
      Route('/tsk/update_ipn/<account>' , name='billing/payment/update_ipn'   , handler='apps.backend.payment.UpdateIPN'),
      Route('/tsk/que_onda/<key>'       , name='billing/payment/que_onda'     , handler='apps.backend.payment.QueOnda'),
      
      # Todas las rutas de billing
      PathPrefixRoute('/billing', [
          
        PathPrefixRoute('/payment', [
          Route('/<invoice>/payment-cancel'   , name='billing/payment/cancel'       , handler='apps.backend.payment.Cancel'),
          Route('/<invoice>/payment-done'     , name='billing/payment/done'         , handler='apps.backend.payment.Done'),
          Route('/<invoice>/payment-pending'  , name='billing/payment/pending'      , handler='apps.backend.payment.Pending'),
        ]),
      ]),
      
      # Todas las rutas de administracion
      Route('/admin'                     , name='backend/index/'                 , handler='apps.backend.auth.Index'),
      
      PathPrefixRoute('/admin', [
        
        Route('/'                        , name='backend/auth/'                  , handler='apps.backend.auth.Index'),
        Route('/help'                    , name='backend/help'                   , handler='apps.backend.help.Index'),
        Route('/login'                   , name='backend/auth/login'             , handler='apps.backend.auth.Login'),
        Route('/signup'                  , name='backend/auth/signup'            , handler='apps.backend.auth.SignUp'),
        Route('/signup/<promo>'          , name='backend/auth/signup/promo'      , handler='apps.backend.auth.SignUp'),
        Route('/logout'                  , name='backend/auth/logout'            , handler='apps.backend.auth.Logout'),
        Route('/restore/password/<key>'  , name='backend/auth/restore'           , handler='apps.backend.auth.RestorePassword'),
        Route('/unrestore/password/<key>', name='backend/auth/unrestore'         , handler='apps.backend.auth.UnRestorePassword'),
        Route('/restore/request'         , name='backend/auth/restore/request'   , handler='apps.backend.auth.RestorePasswordRequest'),
        Route('/validate/<key>'          , name='backend/validate/user'          , handler='apps.backend.auth.ValidateUser'),
        
        PathPrefixRoute('/consultas', [
          Route('/list'                  , name='backend/consultas/list'         , handler='apps.backend.consultas.Index'),
          Route('/list/<page>'           , name='backend/consultas/list/page'    , handler='apps.backend.consultas.Index:page'),
        ]),
        
        PathPrefixRoute('/realestate', [
          Route('/edit'                  , name='backend/realestate/edit'             , handler='apps.backend.realestate.Edit'),
          Route('/request_import'        , name='backend/realestate/request_import'   , handler='apps.backend.realestate.RequestImport'),
        ]),
        
        PathPrefixRoute('/website', [
          Route('/edit'                  , name='backend/realestate_website/edit'             , handler='apps.backend.realestate_website.Edit'),
          Route('/validate_domain_id'    , name='backend/realestate_website/check_domain_id'  , handler='apps.backend.realestate_website.CheckDomainId'),
          Route('/set_theme/<theme>'     , name='backend/realestate_website/set_theme'        , handler='apps.backend.realestate_website.Edit:set_theme')
        ]),
        
        PathPrefixRoute('/inmobiliarias_amigas', [
          Route('/list'                         , name='backend/realestatebook/list'                    , handler='apps.backend.realestatebook.Index'),
          Route('/requests'                     , name='backend/realestatebook/requests'                , handler='apps.backend.realestatebook.Requests'),
          Route('/friends'                      , name='backend/realestatebook/friends'                 , handler='apps.backend.realestatebook.Friends'),
          Route('/friends/delete/<key>'         , name='backend/realestatebook/friends/delete'          , handler='apps.backend.realestatebook.Friends:delete'),
          Route('/friends/share/<key>'          , name='backend/realestatebook/friends/share'           , handler='apps.backend.realestatebook.Friends:share'),
          Route('/friends/unshare/<key>'        , name='backend/realestatebook/friends/unshare'         , handler='apps.backend.realestatebook.Friends:unshare'),
          Route('/friend_request'               , name='backend/realestatebook/friend_request'          , handler='apps.backend.realestatebook.FriendRequest'),
          Route('/friend_request/accept/<key>'  , name='backend/realestatebook/friend_request/accept'   , handler='apps.backend.realestatebook.FriendRequest:accept'),
          Route('/friend_request/reject/<key>'  , name='backend/realestatebook/friend_request/reject'   , handler='apps.backend.realestatebook.FriendRequest:reject'),
        ]),
		
        
        PathPrefixRoute('/user', [
          Route('/edit'                  , name='backend/user/edit'               , handler='apps.backend.user.Edit'),
          Route('/change_password'       , name='backend/user/change_password'    , handler='apps.backend.user.Edit:password'),
        ]),
        
        PathPrefixRoute('/property', [
          Route('/new'                   , name='property/new'           , handler='apps.backend.property.NewEdit'),
          Route('/<key>/edit/'           , name='property/edit'          , handler='apps.backend.property.NewEdit'),
          Route('/list'                  , name='property/list'          , handler='apps.backend.property.List'),
          Route('/list/<page>'           , name='property/listpage'      , handler='apps.backend.property.List'),
          Route('/update_index'          , name='property/update_index'  , handler='apps.backend.property.UpdateIndex'),
          Route('/<key>/images'          , name='property/images'        , handler='apps.backend.property.Images'),
          Route('/<key>/remove'          , name='property/remove'        , handler='apps.backend.property.Remove'),
          Route('/remove'                , name='property/bulkremove'    , handler='apps.backend.property.Remove'),
          Route('/<key>/restore'         , name='property/restore'       , handler='apps.backend.property.Restore'),
          Route('/<key>/publish/<yes>'   , name='property/publish'       , handler='apps.backend.property.Publish'),
        ]),
        
        PathPrefixRoute('/images', [
          Route('/reorder'               , name='images/reorder'    , handler='apps.backend.images.Reorder'),
          Route('/<key>/upload/'         , name='images/upload'     , handler='apps.backend.images.Upload'),
          Route('/<key>/remove/'         , name='images/remove'     , handler='apps.backend.images.Remove'),
          Route('/<key>/bulkremove/'     , name='images/bulkremove' , handler='apps.backend.images.Remove'),
        ]),
        
        PathPrefixRoute('/account', [
          Route('/status'               , name='backend/account/status'         , handler='apps.backend.account.Status'),
        ]),
        
        
      ])
    ]

    return rules
