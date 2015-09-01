#!/usr/bin/env python
# coding=utf-8
from base import *
from safe import *


class AddProjectHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        name=self.get_argument('projectname')
        info=self.get_argument('info')
        owner_id=self.get_cookie('uid')
        owner_name=self.get_cookie('username')
        dic={
            'name':name,
            'info':info,
            'owner_id':owner_id,
            'owner_name':owner_name
        }

        if self.db.insert('project',dic)!=1:
            pid=self.db.get_id()
            print("add project success")
            self.return_json({'result':200,'pid':pid})
        else:
            self.return_json({'result':100006,'explain':'addproject error'})
            print("error,happened when add project")
            return None
        
class UpdateProjectHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        name=self.get_argument('projectname')
        info=self.get_argument('info')
        owner_name=self.get_cookie('username')
        dic={
            'name':name,
            'info':info,
            'owner_name':owner_name
        }
        if self.db.update('project',dic,{'pid':pid,'owner_id':uid})!=1:
            self.return_json({'result':200})
            print("update project success")
        else:
            self.return_json({'result':100004,'explain':'update_project error'})
            return None

class DelProjectHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        self.del_something('project',pid,uid)    
      

class ShareProjectHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        if self.db.update('project',{'share':1},{'owner_id':uid,'pid':pid})!=1:
            self.return_json({'result':200})
            print("share project success")
        else:
            self.return_json({'result':100005,'explain':'share error'})
            print("share error")
            return None


class UnShareProjectHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        if self.db.update('project',{'share':0},{'owner_id':uid,'pid':pid})!=1:
            self.return_json({'result':200})
            print("unshare project success")
        else:
            self.return_json({'result':100005,'explain':'unshare error'})
            print("share error")
            return None

class ChangeProjectShareStats(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        result=self.db.select('project',{'pid':pid,'owner_id':uid},'share')
        if result!=1:
            sharestats=int(result[0]['share'])
            sharestats=int(not sharestats)
            if self.db.update('project',{'share':sharestats},{'pid':pid})!=1:
                print('ChangeProjectShareStats success')
                self.return_json({'result':200})
            else:
                print("found,but change error")
                self.return_json({'result':100007,'explain':'found,but change error'})
                return None
        else:
            print("not found project")
            self.return_json({'result':100008,'explain':'not found project'})
            return None

class GetProjectInfo(BaseHandler):
    def post(self):
        pid=self.get_argument('pid')
        self.get_info('project',pid) 
