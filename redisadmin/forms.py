#!/usr/bin/env python
#coding=utf-8
import tornado.locale

from redisadmin.extensions.forms import Form, TextField, PasswordField, SubmitField, \
        HiddenField, required


def create_forms():
    
    _forms = {}
    
    for locale in tornado.locale.get_supported_locales(None):

        _ = tornado.locale.get(locale).translate
    
        class FormWrapper(object):

            class LoginForm(Form):
                username = TextField(_("Username"), validators=[
                                  required(message=\
                                           _("You must provide an username"))])

                password = PasswordField(_("Password"))

                next = HiddenField()

                submit = SubmitField(_("Login"))

            
        _forms[locale] = FormWrapper

    return _forms

