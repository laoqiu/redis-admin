#!/usr/bin/env python
#coding=utf-8
import os

DEBUG = True
COOKIE_SECRET = 'simple'
LOGIN_URL = '/login'
XSRF_COOKIES = True

USERNAME = 'admin'
PASSWORD = '111'

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')

DEFAULT_LOCALE = 'en_US' #'zh_CN'

REDIS_SERVER = True
REDIS_DB = 16

# If set to None or 0 the session will be deleted when the user closes the browser.
# If set number the session lives for value days.
PERMANENT_SESSION_LIFETIME = 1 # days

PER_PAGE = 100

try:
    from local_settings import *
except:
    pass

