#!/usr/bin/env python
# coding=utf-8
from base import *
from safe import *

class AddTaskHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        library=self.get_argument('library')
        
        task_name=self.get_argument('taskname')
        task_info=self.get_argument('taskinfo')
        score=self.get_argument('score')
        try:
            time_limit=self.get_argument('limit')
        except:
            time_limit=-1
        pid=self.get_argument('pid')
        dic={
            'uid':uid,
            'pid':pid,
            'task_name':task_name,
            'task_info':task_info,
            'score':score,
            'library':library,
            'time_limit':time_limit
        }
        if self.db.insert('task',dic)!=1:
            id=self.db.get_id()
            print('add_task success')
            result = {
                'result':200,
                'taskid':id
            }
            self.return_json(result)
        else:
            print('error,happened when add_task')
            return None

class UpdateTaskHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        tid=self.get_argument('tid')
        library=self.get_argument('library')
        task_name=self.get_argument('taskname')
        task_info=self.get_argument('taskinfo')
        score=self.get_argument('score')
        try:
            time_limit=self.get_argument('limit')
        except:
            time_limit=-1
        pid=self.get_argument('pid')
        dic={
            'uid':uid,
            'pid':pid,
            'task_name':task_name,
            'task_info':task_info,
            'score':score,
            'library':library,
            'time_limit':time_limit
        } 
        if self.db.update('task',dic,{'tid':tid})!=1:
            print("update_task success")
            self.return_json({'result':200})
        else:
            print("error,happened when update_task")
            return None


class DelTaskHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        tid=self.get_argument('tid')
        self.del_something('task',tid,uid)



class CompeleteTaskHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        tid=self.get_argument('tid')
        result=self.db.select('task',{'tid':tid},'score,time_remain')
        if result==1:
            self.return_json({'result':100003,'explain':'task not found'})
            return 1
        if result[0]['time_remain']!=0:
            time=int(result[0]['time_remain'])
            score=int(result[0]['score'])
            userinfo=self.db.select('userinfo',{'uid':uid},'today_score')
            todayscore=int(userinfo[0]['today_score'])+score
            try:
                self.db.update('userinfo',{'today_score':todayscore},{'uid':uid}) 
                self.db.update('task',{'time_remain':time-1},{'tid':tid})
            except:
                return None
            print("compeletetask sucess")
            self.return_json({'result':200})
        else:
            print("error,happened when compeletetask")
            self.return_json({'result':100002,'explain':'time_remain is 0'})
            return None

class GetTaskInfo(BaseHandler):
    def post(self):
        tid=self.get_argument('tid')
        self.get_info('task',tid)

class GetAllLibraryOfOneUser(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        uid=self.get_cookie('uid')
        result=self.db.select('task',{'uid':uid},'library')
        if result!=1:
            self.return_json({'result':200,'library':result})
            print('return library success')
        else:
            self.return_json({'result':100010,'explain':'no library'})
            print('no library found')
            return None

class GetNowTask(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        uid=self.get_cookie('uid')
        nowpid=self.db.select('userinfo',{'uid':uid},'nowpid')[0]['nowpid']
        print(nowpid)
        result=self.db.select('task',{'uid':uid,'pid':nowpid})
        if result!=1:
            self.return_json({'result':200,'task':result})
            print('get now task success')
        else:
            self.return_json({'result':100012,'explain':'no this user or this project'})
            print('error when get now task')
            return None

