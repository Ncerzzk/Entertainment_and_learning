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
        a=self.get_argument('a') or 'hello'
        print(a)
                
        
class GetHTMLHandler(BaseHandler):
    def get(self,path,file):
        fname=path+'/'+file
        self.return_html(fname)
 
class UserInfoHandler(BaseHandler):
    def post(self):
        pass

class UpdateUserInfoHandler(BaseHandler):
    def post(self):
        pass 

application = tornado.web.Application([
        (r"/test",TestHandler),
        (r"/user/reg", RegHandler),
        (r"/user/confirmpwd",ConfirmPasswordHandler),
        (r"/user/login",LoginHandler),
        (r"/user/get",GetUserInfo),
        (r"/user/logout",LogoutHandler),
        (r"/user/update",UpdateUserHandler),
        (r"/task/add",AddTaskHandler),
        (r"/task/update",UpdateTaskHandler),
        (r"/task/del",DelTaskHandler),
        (r"/task/get",GetTaskInfo),
        (r"/task/compelete",CompeleteTaskHandler),
        (r"/task/getlibrary",GetLibraryHandler),
        (r"/task/getnowtask",GetNowTask),
        (r"/task/gettask",GetTask),
        (r"/project/add",AddProjectHandler),
        (r"/project/setnowpid",SetNowPidHandler),
        (r"/project/del",DelProjectHandler),
        (r"/project/update",UpdateProjectHandler),
        (r"/project/share",ShareProjectHandler),
        (r"/project/unshare",UnShareProjectHandler),
        (r"/project/change",ChangeProjectShareStats),
        (r"/project/get",GetProjectInfo),
        (r"/project/getall",GetAllProjectHandler),
        (r"/project/getshared",GetAllSharedProjectHandler),
        (r"/project/fork",ForkProjectHandler),
        (r"/(.+?)/(.+?)",GetHTMLHandler)

],cookie_secret=SECRET)

application.listen(80)
tornado.ioloop.IOLoop.instance().start()
