#!/usr/bin/env python
# coding=utf-8
from base import *
from safe import *

class TaskError(Error):
    pass

class UserUnfitError(TaskError):
    def __str__(self):
        return 'error,the user is not the project owner.'

class TimeLimitError(TaskError):
    def __str__(self):
        return 'the task compelete time has been over the limit.'


class TaskHandler(BaseHandler):
    def add_task(self,uid,pid,task_name,task_info,score,library,time_limit):
        """
        arguments:
        uid,pid,task_name,task_info,score,library,time_limit
        return:
        e11 the user not the owner 
        e12 no found project
        e13 add error
        """
        #check the user is the project owner
        owner=self.db.select('project',{'pid':pid},'owner_id')
        if owner!=1:
            if owner[0]['owner_id']!=uid:
                raise UserUnfitError
        else:
            raise NoFoundError('Task')
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
            raise AddError
    
    def compelete_task(self,uid,tid):
        result=self.db.select('task',{'tid':tid},'score,time_remain')
        if result==1:
            raise NoFoundError('Task')
        if result[0]['time_remain']!=0:
            time=int(result[0]['time_remain'])
            score=int(result[0]['score'])
            userinfo=self.db.select('userinfo',{'uid':uid},'today_score')
            todayscore=int(userinfo[0]['today_score'])+score
            if self.update_one('userinfo',{'uid':uid},today_score=todayscore)==1:
                raise NoFoundError('User')
            if self.update_one('task',{'tid':tid},time_remain=time-1)==1:
                raise NoFoundError('Task')
        else:
            raise TimeLimitError

    def get_task(self,pid):
        result=self.db.select('task',{'pid':pid})
        if result!=1:
            return result
        else:
            raise NoFoundError('Task')

    def get_nowtask(self,uid):
        nowpid=self.db.select('userinfo',{'uid':uid},'nowpid')[0]['nowpid']
        result=self.db.select('task',{'uid':uid,'pid':nowpid})
        if result!=1:
            return result
        else:
            raise NoFoundError("Now Tasks")


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
            raise NoFoundError('Library')

    def del_task(self,tid,uid):
        #check if the user is the task owner
        owner=self.db.select('task',{'tid':tid},'uid') 
        if owner==1:
            raise NoFoundError('Task')
        if owner[0].uid!=uid:
            raise UserUnfitError
        self.del_something('task',tid,uid)



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
        try:
            id=self.add_task(uid=uid,library=library,task_name=task_name,task_info=task_info,score=score,time_limit=time_limit,pid=pid)
        except AddError as e:
            self.return_json({'result':100001,'explain':str(e)})
        except NoFoundError as e:
            self.return_json({'result':100004,'explain':str(e)})
        except UserUnfitError as e:
            self.return_json({'result':100005,'explain':str(e)})
        else:
            self.return_json({'result':200,'tid':id})



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
        try:
            self.del_task(tid,uid)
        except UserUnfitError as e:
            self.return_json({'result':100005,'explain':str(e)})
        except NoFoundError as e:
            self.return_json({'result':100004,'explain':str(e)})
        else:
            self.return_json({'result':200})

class CompeleteTaskHandler(TaskHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        tid=self.get_argument('tid')
        try:
            self.compelete_task(uid,tid)
        except NoFoundError as e:
            self.return_json({'result':100004,'explain':str(e)})
        except TimeLimitError as e:
            self.return_json({'result':100006,'explain':str(e)})
        else:
            self.return_json({'result':200,'tid':tid})

class GetTaskInfo(TaskHandler):
    def post(self):
        tid=self.get_argument('tid')
        try:
            result=self.get_info('task',tid)
        except NoFoundError as e:
            self.return_json({'result':100004,'explain':str(e)})
        else:
            self.return_json({'result':200,'taskinfo':result})

class GetLibraryHandler(TaskHandler):
    @tornado.web.authenticated
    def get(self):
        uid=self.get_cookie('uid')
        try:
            result=self.get_library(uid)
        except NoFoundError as e:
            self.return_json({'result':100004,'explain':str(e)})
        else:
            self.return_json({'result':200,'library':result})
        
class GetNowTask(TaskHandler):
    @tornado.web.authenticated
    def get(self):
        uid=self.get_cookie('uid')
        try:
            result=self.get_nowtask(uid)
        except NoFoundError as e:
            self.return_json({'result':100004,'explain':str(e)})
        else:
            self.return_json({'result':200,'task':result})

class GetTask(TaskHandler):
    def post(self):
        pid=self.get_argument('pid')
        try:
            result=self.get_task(pid)
        except NoFoundError as e:
            self.return_json({'result':100004,'explain':str(e)})
        else:
            self.return_json({'result':200,'task':result})
