# -*- coding: utf-8 -*-
import logging

from webapp2_extras.json import json
from search_helper import config_array
from utils import FrontendHandler
from models import Property

class Index(FrontendHandler):
  def get(self, **kwargs):
    preset = {'prop_operation_id':str(Property._OPER_SELL)}
    return self.render_response('frontend/home.html'
                , config_array=config_array
                , preset=preset
                , presetJSON=json.dumps(preset)
                , _OPER_SELL=Property._OPER_SELL
                , _OPER_RENT=Property._OPER_RENT)