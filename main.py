#!/usr/bin/env python
# encoding: utf-8

import time
import hashlib
import json
import re
import pymysql
import tornado.ioloop
import tornado.web

from db import *
from safe import *
from setting import *
from base import *
from user import *
from task import *
from project import *
            
class TestHandler(BaseHandler):
    def post(self):
        self.db.del_one('task',{'uid':1})
                
        
class GetHTMLHandler(BaseHandler):
    def get(self):
        self.return_html('reg.html')
 
class UserInfoHandler(BaseHandler):
    def post(self):
        pass

class UpdateUserInfoHandler(BaseHandler):
    def post(self):
        pass 
"""
a=DB('localhost','root','6789mm','learning')
# a.insert('user',{'name':'hello','password':'1234' })
a.del_one('user',{'name':'hello'})
print(a.select('user',{'id':5}))
"""

application = tornado.web.Application([
        (r"/test",TestHandler),
        (r"/user/reg", RegHandler),
        (r"/user/login",LoginHandler),
        (r"/user/get",GetUserInfo),
        (r"/user/logout",LogoutHandler),
        (r"/task/add",AddTaskHandler),
        (r"/task/update",UpdateTaskHandler),
        (r"/task/del",DelTaskHandler),
        (r"/task/get",GetTaskInfo),
        (r"/task/compelete",CompeleteTaskHandler),
        (r"/project/add",AddProjectHandler),
        (r"/project/del",DelProjectHandler),
        (r"/project/update",UpdateProjectHandler),
        (r"/project/share",ShareProjectHandler),
        (r"/project/unshare",UnShareProjectHandler),
        (r"/project/change",ChangeProjectShareStats),
        (r"/project/get",GetProjectInfo),
        (r"/reg.html",GetHTMLHandler)

])

application.listen(8888)
tornado.ioloop.IOLoop.instance().start()
