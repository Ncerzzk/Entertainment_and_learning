#!/usr/bin/env python
# coding=utf-8
from base import *
from safe import *

class TaskHandler(BaseHandler):
    def add_task(self,uid,pid,task_name,task_info,score,library,time_limit):
        """
        arguments:
        uid,pid,task_name,task_info,score,library,time_limit
        """
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
            return id
        else:
            return None
    
    def compelete_task(self,uid,tid):
        result=self.db.select('task',{'tid':tid},'score,time_remain')
        if result==1:
            self.return_json({'result':100003,'explain':'task not found'})
            return None
        if result[0]['time_remain']!=0:
            time=int(result[0]['time_remain'])
            score=int(result[0]['score'])
            userinfo=self.db.select('userinfo',{'uid':uid},'today_score')
            todayscore=int(userinfo[0]['today_score'])+score
            try:
                self.update_one('userinfo',{'uid':uid},today_score=todayscore)
                self.update_one('task',{'tid':tid},time_remain=time-1)
                return 'success'
            except Exception as e:
                print(e)
                return None
        else:
            return None
    def get_task(self,pid):
        result=self.db.select('task',{'pid':pid})
        if result!=1:
            return result
        else:
            return None

    def get_nowtask(self,uid):
        nowpid=self.db.select('userinfo',{'uid':uid},'nowpid')[0]['nowpid']
        result=self.db.select('task',{'uid':uid,'pid':nowpid})
        if result!=1:
            return result
        else:
            return None


    def get_library(self,uid):
        pid=self.db.select('userinfo',{'uid':uid},'nowpid')
        pid=pid[0]['nowpid']
        result=self.db.select('task',{'uid':uid,'pid':pid},'library')

        if result!=1:
            library=[]
            for i in result:
                if i['library'] not in library:
                    library.append(i['library'])
            return library
        else:
            return None



class AddTaskHandler(TaskHandler):
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
        id=self.add_task(uid=uid,library=library,task_name=task_name,task_info=task_info,score=score,time_limit=time_limit,pid=pid)
        if id!=None:
            self.return_json({'result':200,'tid':id})
        else:
            self.return_json({'result':100013,'explain':'addtask error'})



class UpdateTaskHandler(TaskHandler):
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
        condition={'tid':tid}
        if self.update_one('task',condition,uid=uid,pid=pid,library=library,task_name=task_name,task_info=task_info,score=score,time_limit=time_limit)!=None: 
            self.return_json({'result':200,'tid':tid})
        else:
            self.return_json({'result':100014,'explain':'update error'})


class DelTaskHandler(TaskHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        tid=self.get_argument('tid')
        self.del_something('task',tid,uid)

class CompeleteTaskHandler(TaskHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        tid=self.get_argument('tid')
        if self.compelete_task(uid,tid)!=None:
            self.return_json({'result':200,'tid':tid})
        else:
            self.return_json({'result':100002,'explain':'compeletetask error'})

class GetTaskInfo(TaskHandler):
    def post(self):
        tid=self.get_argument('tid')
        result=self.get_info('task',tid)
        if result!=None:
            self.return_json({'result':200,'taskinfo':result})
        else:
            self.return_json({'result':100021,'explain':'error,gettaskinfo'})

class GetLibraryHandler(TaskHandler):
    @tornado.web.authenticated
    def get(self):
        uid=self.get_cookie('uid')
        result=self.get_library(uid)
        if result!=None:
            self.return_json({'result':200,'library':result})
        else:
            self.return_json({'result':100010,'explain':'no library'})
        
class GetNowTask(TaskHandler):
    @tornado.web.authenticated
    def get(self):
        uid=self.get_cookie('uid')
        result=self.get_nowtask(uid)
        if result!=None:
            self.return_json({'result':200,'task':result})
        else:
            self.return_json({'result':100012,'explain':'no this user or this project'})

class GetTask(TaskHandler):
    def post(self):
        pid=self.get_argument('pid')
        result=self.get_task(pid)
        if result!=None:
            self.return_json({'result':200,'task':result})
        else:
            self.return_json({'result':100012,'explain':'no this user or this project'})
