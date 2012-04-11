#!/usr/bin/env python
#coding=utf-8
"""
    helpers.py
    ~~~~~~~~~~~~~
    :author: laoqiu.com@gmail.com
"""

class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.
    >>> o = storage(a=1)
    >>> o.a
    1
    >>> o['a']
    1
    >>> o.a = 2
    >>> o['a']
    2
    >>> del o.a
    >>> o.a
    Traceback (most recent call last):
    ...
    AttributeError: 'a'
    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k
    
    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'


def setting_from_object(obj):
    settings = dict()
    for key in dir(obj):
        if key.isupper():
            settings[key.lower()] = getattr(obj, key)
    return settings


class Pagination(object):
    def __init__(self, query, page, per_page):
        self.query = query
        self.per_page = per_page
        self.page = page

    @property
    def total(self):
        return len(self.query)
    
    @property
    def items(self):
        return self.query[(self.page - 1) * self.per_page : self.page * self.per_page]

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
        
    has_prev = property(lambda x: x.page > 1)
    prev_num = property(lambda x: x.page - 1)
    has_next = property(lambda x: x.page < x.pages)
    next_num = property(lambda x: x.page + 1)
    pages = property(lambda x: max(0, x.total - 1) // x.per_page + 1)


storage = Storage

