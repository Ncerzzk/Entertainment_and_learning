#!/usr/bin/env python
# coding=utf-8
from base import *
from safe import *

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
            return None

   
    def set_share_stat(self,pid,uid,stat):
        if self.update_one('project',{'pid':pid,'owner_id':uid},share=stat)!=1:
            return 'success'
        else:
            return None

    def set_now_pid(self,pid,uid):
        if self.db.update('userinfo',{'nowpid':pid},{'uid':uid})!=1:
            return 'success'
        else:
            self.return_json({'result':100011,'explain':'no this user'})
            return None

    def get_all_projects(self,uid):
        result=self.db.select('project',{'owner_id':uid})
        if result!=1:
            return result
        else:
            return None
          



class AddProjectHandler(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        name=self.get_argument('projectname')
        info=self.get_argument('info')
        owner_id=self.get_cookie('uid')
        owner_name=self.get_cookie('username')
        pid=self.add_project(name,info,owner_id,owner_name)
        if pid!=None:
            self.return_json({'result':200,'pid':pid})
        else:
            self.return_json({'result':100006,'explain':'addproject error'})
            return None
        
class UpdateProjectHandler(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        name=self.get_argument('projectname')
        info=self.get_argument('info')
        owner_name=self.get_cookie('username')
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
        self.del_something('project',pid,uid)    
      

class ShareProjectHandler(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        if self.set_share_stat(pid,uid,1)!=None:
            self.return_json({'result':200})
        else:
            self.return_json({'result':100005,'explain':'share error'})
            return None

class SetNowPidHandler(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        if self.set_now_pid(pid,uid)!=None:
            self.return_json({'result':200})
        else:
            self.return_json({'result':100011,'explain':'no this user'})
            return None


class UnShareProjectHandler(ProjectHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        if self.set_share_stat(pid,uid,0)!=None:
            self.return_json({'result':200})
        else:
            self.return_json({'result':100005,'explain':'unshare error'})
            return None


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
        self.get_info('project',pid) 

class GetAllProjectHandler(ProjectHandler):
    @tornado.web.authenticated
    def get(self):
        uid=self.get_cookie('uid')
        result=self.get_all_projects(uid)
        if result!=None:
            self.return_json({'result':200,'projects':result})
        else:
            self.return_json({'result':100019,'explain':'no projects'})
