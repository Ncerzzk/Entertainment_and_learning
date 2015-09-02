#!/usr/bin/env python
# coding=utf-8
from db import *
import tornado.web
import json
from setting import *


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db=DB(DBHOST,DBUSER,DBPWD,DBNAME)


    def return_json(self,obj):
        self.set_header('Content-type','application/json')
        self.write(json.dumps(obj))

    def get_current_user(self):
        uid=self.get_cookie('uid')
        session=self.get_cookie('session')
        username=self.get_cookie('username')
        if uid==None:
            return None
        result=self.db.select('session',{'uid':uid,'session':session},'deadline')[0]
        deadline=int(result['deadline'])
        if result!=1:
            now_time=Safe.get_time()
            if int(now_time)>deadline:
                """
                out time
                """
                return None
            else:
                return username
        else:
            return None

    def del_something(self,table,id,uid=None):
        idname=table[:1:]+'id'
        if uid is None:
            condition={
                idname:id
            }
        else:
            condition={
                'uid':uid,
                idname:id
            }
        result=self.db.del_one(table,condition)
        if result==1:
            self.return_json({'result':100003,'explain':' not found'})
            print("error,del")
            return None
        else:
            print("del success")
            self.return_json({'result':200})

    def get_info(self,table,id):
        idname=table[:1:]+'id'
        condition={
            idname:id
        }        
        result=self.db.select(table,condition)
        if result !=1:
            self.return_json(result[0])
            print('get %s info,success'%table)
        else:
            print('erro,get project info')
            self.return_json({'result':100009,'explain':'get %s info error'% table})
            return None


