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
      Route('/ver/<archivo>'    , name='ver_archivo'  , handler='apps.backend.property.VerArchivo'),
      
      Route('/admin'                     , name='backend/index/'                  , handler='apps.backend.auth.Index'),
      PathPrefixRoute('/admin', [
        
        Route('/'                        , name='backend/auth/'                  , handler='apps.backend.auth.Index'),
        Route('/login'                   , name='backend/auth/login'             , handler='apps.backend.auth.Login'),
        Route('/signup'                  , name='backend/auth/signup'            , handler='apps.backend.auth.SignUp'),
        Route('/logout'                  , name='backend/auth/logout'            , handler='apps.backend.auth.Logout'),
        Route('/restore/password/<key>'  , name='backend/auth/restore'           , handler='apps.backend.auth.RestorePassword'),
        Route('/unrestore/password/<key>', name='backend/auth/unrestore'         , handler='apps.backend.auth.UnRestorePassword'),
        Route('/restore/request'         , name='backend/auth/restore/request'   , handler='apps.backend.auth.RestorePasswordRequest'),
        Route('/validate/<key>'          , name='backend/validate/user'          , handler='apps.backend.auth.ValidateUser'),
        
        PathPrefixRoute('/realestate', [
          Route('/edit'                  , name='backend/realestate/edit'   , handler='apps.backend.realestate.Edit'),
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
          Route('/<key>'                 , name='images/original'   , handler='apps.backend.images.Show:original'),
          Route('/<key>/<width>/<height>', name='images/show'       , handler='apps.backend.images.Show'),
          Route('/<key>/upload/'         , name='images/upload'     , handler='apps.backend.images.Upload'),
          Route('/<key>/remove/'         , name='images/remove'     , handler='apps.backend.images.Remove'),
          Route('/<key>/bulkremove/'     , name='images/bulkremove' , handler='apps.backend.images.Remove'),
        ]),
        
        PathPrefixRoute('/account', [
          Route('/status'               , name='backend/account/status'    , handler='apps.backend.account.Status'),
        ]),
        
        
      ])
    ]

    return rules
