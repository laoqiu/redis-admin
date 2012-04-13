#!/usr/bin/env python
#coding=utf-8
"""
    redisadmin Application
    ~~~~~~~~~~~
    :author: laoqiu.com@gmail.com
"""
import os
import redis

import tornado.web
import tornado.locale

from redisadmin import settings as config
from redisadmin import uimodules
from redisadmin.helpers import setting_from_object
from redisadmin.forms import create_forms
from redisadmin.views import ErrorHandler, frontend
from redisadmin.extensions.routing import Route
from redisadmin.extensions.sessions import RedisSessionStore

class Application(tornado.web.Application):
    def __init__(self):
        settings = setting_from_object(config)
        handlers = [
            # other handlers...
        ] + Route.routes()
        
        # Custom 404 ErrorHandler
        handlers.append((r"/(.*)", ErrorHandler)) 
        
        settings.update(dict(
            ui_modules = uimodules,
            autoescape = None
        ))
        
        if 'default_locale' in settings:
            tornado.locale.load_gettext_translations(
                os.path.join(os.path.dirname(__file__), 'translations'), 'messages')

        tornado.web.Application.__init__(self, handlers, **settings)
        
        self.forms = create_forms()
        self.redis = [redis.StrictRedis(db=n) for n in range(self.settings['redis_db'])]
        self.session_store = RedisSessionStore(self.redis[0])
        


