#!/usr/bin/env python
# coding=utf-8
from base import *
from safe import *
from error import *

class ProjectError(Error):
    pass

class UserUnfitError(ProjectError):
    def __str__(self):
        return 'the user is not the owner of the project'


class ProjectHandler(BaseHandler):
    def add_project(self,projectname,info,owner_id,owner_name):
        dic={
            'name':projectname,
            'info':info,
            'owner_id':owner_id,
            'owner_name':owner_name
        }
        if self.db.insert('project',dic)!=1:
            id=self.db.get_id()
            return id
        else:
            raise AddError('Project')

   
    def set_share_stat(self,pid,uid,stat):
        #check owner
        uid=int(uid)
        owner=self.db.select('project',{'pid':pid},'owner_id')
        if owner==1:
            raise NoFoundError('project')
        elif owner[0]['owner_id']!=uid:
            raise UserUnfitError()
        self.update_one('project',{'pid':pid,'owner_id':uid},share=stat)

    def set_now_pid(self,pid,uid):
        user=self.db.select('userinfo',{'uid':uid})
        if user==1:
            raise NoFoundError('User')
        self.db.update('userinfo',{'nowpid':pid},{'uid':uid})

    def get_all_projects(self,uid):
        user=self.db.select('userinfo',{'uid':uid})
        if user==1:
            raise NoFoundError('User')      
        result=self.db.select('project',{'owner_id':uid})
        if result==1:
            raise NoFoundError('Project')
        else:
            return result

    def get_all_shared_projects(self,page=1):
        result=self.db.select('project',{'share':1})
        if result!=1:
            return result
        else:
            raise NoFoundError('Project')  

    def fork_project(self,pid,uid):
        result=self.db.select('project',{'pid':pid})
        #now get username
        username=self.db.select('userinfo',{'uid':uid},'name')
        if username==1:
            raise NoFoundError('User')
        if result!=1:
            result=result[0]
            #add fork count
            self.update_one('project',{'pid':pid},fork_count=int(result['fork_count'])+1)
            result.pop('pid')
            result['owner_id']=uid
            result['owner_name']=username[0]['name']
            result['share']=0
            result['fork_count']=0
            self.db.insert('project',result)
            newpid=self.db.get_id()
            #now start copy task
            tasks=self.db.select('task',{'pid':pid})
            if tasks !=1:
                for i in tasks:
                    i.pop('tid')
                    i['pid']=newpid
                    self.db.insert('task',i)
                return newpid
            else:
                return None
        else:
            raise NoFoundError('project')


class AddProjectHandler(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        name=self.get_argument('projectname')
        info=self.get_argument('info')
        owner_id=self.get_cookie('uid')
        username=self.db.select('user',{'uid':owner_id},'name')
        owner_name=username[0]['name']
        try:
            pid=self.add_project(name,info,owner_id,owner_name)
        except Error as e:
            self.return_json({'result':100000,'explain':str(e)})
        else:
            self.return_json({'result':200,'pid':pid})
        
class UpdateProjectHandler(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        name=self.get_argument('projectname')
        info=self.get_argument('info')
        username=self.db.select('user',{'uid':owner_id},'name')
        owner_name=username[0]['name'] 
        if self.update_one('project',{'pid':pid,'owner_id':uid},name=name,info=info,owner_name=owner_name)!=None:
            self.return_json({'result':200})
        else:
            self.return_json({'result':100004,'explain':'update_project error'})
            return None

class DelProjectHandler(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        try:
            self.del_something('project',pid,uid)
        except Error as e:
            self.return_json({'result':100000,'explain':str(e)})
        else:
            self.return_json({'result':200})
      

class ShareProjectHandler(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        try: 
            self.set_share_stat(pid,uid,1)
        except Error as e:
            self.return_json({'result':100000,'explain':str(e)})
        else:
            self.return_json({'result':200})

class SetNowPidHandler(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        try:
            self.set_now_pid(pid,uid)
        except Error as e:
            self.return_json({'result':100000,'explain':str(e)})
        else:
            self.return_json({'result':200})


class UnShareProjectHandler(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        try: 
            self.set_share_stat(pid,uid,0)
        except Error as e:
            self.return_json({'result':100000,'explain':str(e)})
        else:
            self.return_json({'result':200})


class ChangeProjectShareStats(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        result=self.db.select('project',{'pid':pid,'owner_id':uid},'share')
        if result!=1:
            sharestats=int(result[0]['share'])
            sharestats=int(not sharestats)
            if self.set_share_stat(pid,uid,sharestats)!=None:
                self.return_json({'result':200})
            else:
                self.return_json({'result':100007,'explain':'found,but change error'})
                return None
        else:
            self.return_json({'result':100008,'explain':'not found project'})
            return None

class GetProjectInfo(ProjectHandler):
    def post(self):
        pid=self.get_argument('pid')
        try:
            result=self.get_info('project',pid)
        except Error as e:
            self.return_json({'result':100000,'explain':str(e)})
        else:
            self.return_json({'result':200,'projectinfo':result})

class GetAllProjectHandler(ProjectHandler):
    @tornado.web.authenticated
    def get(self):
        uid=self.get_cookie('uid')
        try:
            result=self.get_all_projects(uid)
        except Error as e:
            self.return_json({'result':100000,'explain':str(e)})
        else:
            self.return_json({'result':200,'projects':result})

class GetAllSharedProjectHandler(ProjectHandler):
    def get(self):
        try:
            result=self.get_all_shared_projects()
        except Error as e:
            self.return_json({'result':100000,'explain':str(e)})
        else:
            self.return_json({'result':200,'projects':result})

class ForkProjectHandler(ProjectHandler):
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        try:
            result=self.fork_project(pid,uid)
        except Error as e:
            self.return_json({'result':100000,'explain':str(e)})
        else:
            self.return_json({'result':200,'newpid':result})
