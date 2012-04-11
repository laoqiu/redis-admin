#!/usr/bin/env python
#coding=utf-8
"""
    views: frontend.py
    ~~~~~~~~~~~
    :author: laoqiu.com@gmail.com
"""
# import redis
# import logging
import json
import urllib
import tornado.web

from redisadmin.views import RequestHandler
from redisadmin.helpers import Pagination
from redisadmin.extensions.routing import route


@route("/", name='index')
class Index(RequestHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')
        return 


@route("/menu", name='menu')
class Menu(RequestHandler):
    @tornado.web.authenticated
    def get(self):
        q = self.get_args('q','*')
        
        fullkeys = self.redis.keys(q)

        def get_item(key, root):
            id = '%s:%s' % (root, key) if root else key
            children = get_children(id)
            item = {"text": '%s(%s)' % (id, len(children)) if children else id,
                    "id": id,
                    "children": sorted(children)[:200]
                    }
            return item

        def get_children(root=None):
            if root:
                keys = set(sorted([key[len(root)+1:].split(':')[0] for key in fullkeys if key[:len(root)+1]=='%s:' % root]))
            else:
                keys = set(sorted([key.split(':')[0] for key in fullkeys]))

            return [get_item(key, root) for key in keys]
        

        children = get_children()
        while len(children)==1 and children[0]['children']:
            children = children[0]['children']

        menu = [{"text": '%s(%s)' % (q, len(children)), "id": q, "children": children}]
        
        self.write(json.dumps(menu))
        return 


@route("/value", name='value')
class Value(RequestHandler):
    @tornado.web.authenticated
    def get(self):
        key = self.get_args('key','')
        if key:
            _type = self.redis.type(key)
            if _type=='string':
                value = self.get_strings(key)
            elif _type=='list':
                value = self.get_lists(key)
            elif _type=='hash':
                value = self.get_hashes(key)
            elif _type=='set':
                value = self.get_sets(key)
            elif _type=='zset':
                value = self.get_sortedsets(key)
            else:
                _type = value = None
            
            self.write(dict(type=_type,key=key,value=value))
            return

        self.write(dict(type=None,key=key,value=None))
        return
    
    def get_strings(self, key):
        return self.redis.get(key)
    
    def get_hashes(self, key):
        return self.redis.hgetall(key)

    def get_lists(self, key):
        return self.redis.lrange(key, 0, -1)
    
    def get_sets(self, key):
        return self.redis.smembers(key)
    
    def get_sortedsets(self, key):
        return self.redis.zrange(key, 0, -1)


@route("/list", name='list')
class List(RequestHandler):
    @tornado.web.authenticated
    def get(self):
        root = self.get_args('root','')
        if root:
            
            while (root and root[-1] in [':','*']):
                root = root[:-1]

            page = self.get_args('page', 1, type=int)
            if page < 1: page = 1

            per_page = self.settings['per_page']

            fullkeys = sorted(self.redis.keys(root+':*'))

            data = [(key, self.redis.hgetall(key) if self.redis.type(key)=='hash' else {}) \
                        for key in fullkeys if key.split(root)[-1].count(':')==1]

            page_obj = Pagination(data, page, per_page=per_page)
            
            iter_pages = [p for p in page_obj.iter_pages()]
            
            self.write(dict(data=page_obj.items, root=root, page=page, iter_pages=iter_pages))
            return

        self.write(dict(data=[]))
        return


@route("/info", name="info")
class Info(RequestHandler):
    @tornado.web.authenticated
    def get(self):
        info = self.redis.info()
        self.write(json.dumps(info.items()))
        return 


@route("/flush/db", name="flush_db")
class FlushDB(RequestHandler):
    @tornado.web.authenticated
    def get(self):
        result = self.redis.flushdb()
        self.write(dict(success=result))
        return 


@route("/flush/all", name="flush_all")
class FlushDB(RequestHandler):
    @tornado.web.authenticated
    def get(self):
        result = self.redis.flushall()
        self.write(dict(success=result))
        return 


@route("/expire", name="expire")
class Expire(RequestHandler):
    @tornado.web.authenticated
    def get(self):

        key = self.get_args('key', '')
        seconds = self.get_args('seconds', 0, type=int)

        if key:

            result = self.redis.expire(key, seconds)

            self.write(dict(success=result))
            return 

        self.write(dict(success=False))
        return 


@route("/move", name="move")
class Move(RequestHandler):
    @tornado.web.authenticated
    def get(self):

        key = self.get_args('key', '')
        db = self.get_args('db', -1, type=int)

        if key and db>=0:
            try:
                result = self.redis.move(key, db)
            except:
                result = False

            self.write(dict(success=result))
            return 

        self.write(dict(success=False))
        return 


@route("/delete", name="delete")
class Delete(RequestHandler):
    @tornado.web.authenticated
    def get(self):

        key = self.get_args('key', '')
        if key:
            result = self.redis.delete(key)

            self.write(dict(success=result))
            return 
        
        self.write(dict(success=False))
        return 


@route("/login", name='login')
class Login(RequestHandler):
    def get(self):
        form = self.forms.LoginForm()
        self.render('login.html', form=form)
        return 
     
    def post(self):
        form = self.forms.LoginForm(self.request.arguments)
    
        if form.validate():
            if self.settings['username']==form.username.data and \
                    self.settings['password']==form.password.data:

                self.session['user'] = {'username': self.settings['username']}
                self.session.save()
                
                self.redirect(self.reverse_url('index'))
                return
            else:
                form.submit.errors.append(self._("The username or password you provided are incorrect."))

        self.render('login.html', form=form)
        return 


@route("/logout", name='logout')
class Logout(RequestHandler):
    def get(self):

        del self.session['user']
        self.session.save()

        self.redirect(self.reverse_url('index'))
        return


