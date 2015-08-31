#!/usr/bin/env python
# coding=utf-8

import time
import hashlib
import re


class Safe(object):
    @staticmethod
    def clear(string):
        """
        prevent from sql attack
        """
        r='select|insert|update|delete|drop|into'
        pattern=re.compile(r)
        try:
            string=string.decode('utf-8')
        except:
            pass
        result=re.sub(pattern,'',string)
        return result

    @staticmethod
    def md5(string):
        m=hashlib.md5()
        m.update(string.encode())
        return m.hexdigest()

    @staticmethod
    def get_time():
        return int(time.time())

    @staticmethod
    def get_session(salt):
        t=str(Safe.get_time())
        string=t+str(salt)
        return Safe.md5(string)
    
    @staticmethod
    def get_deadline(days=30):
        t=Safe.get_time()
        t+=24*60*60*days
        return t
