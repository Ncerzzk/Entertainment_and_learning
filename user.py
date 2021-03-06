#!/usr/bin/env python
# coding=utf-8
from base import *
from safe import *

class UserHandler(BaseHandler):
    def add_user(self,mail,password,username): 
        password=Safe.md5(password)
        if self.db.insert('user',{'mail':mail,'password':password,'name':username})!=1:
            uid=self.db.get_id()
            self.db.insert('userinfo',{'uid':uid,'name':username})
            return uid
        else:
            return None

    def confirm_password(self,uid,password):
        password=Safe.md5(password)
        if self.db.select('user',{'uid':uid,'password':password})!=1:
            return 'success'
        else:
            return None
   
    def add_session(self,uid,session,deadline):
        if self.db.insert('session',{'uid':uid,'session':session,'deadline':deadline})!=1:
            sid=self.db.get_id()
            return sid
        else:
            return None

    
    def login(self,mail,password):
        password=Safe.md5(password)
        result = self.db.select('user',{'mail':mail,'password':password},'uid')
        if result==1:
            return None
        result=result[0]
        uid=result['uid']
        self.set_secrue_cookie('uid',str(uid))
        return uid

    def logout(self,uid):
        if self.db.del_one('session',{'uid':uid})!=1:
            self.return_json({'result':200})
            print("logout success")
        else:
            print("error,when logout")

        self.clear_all_cookies()

    def reg(self,mail,password,username=None):
        username=username or 'null'
        """
        rember to clear evil code in mail and password.
        """
        if self.db.select('user',{'mail':mail},'uid')!=1:
            # existed user
            self.return_json({'result':100001,'explain':'the user has signed.'})
            print('user has signed.')
            return None
        uid=self.add_user(mail,password,username)
        if uid !=None:
            self.return_json({'result':200,'uid':uid,'session':session})
            self.set_secrue_cookie('uid',str(uid))

        
    def get_userinfo(self,uid):
        result=self.get_info('userinfo',uid)
        if result!=None:
            return result
        else:
            return None

class LoginHandler(UserHandler):
    def post(self):
        mail=self.get_argument('mail')
        password=self.get_argument('password')
        result=self.login(mail,password)
        if result!=None:
            self.return_json({'uid':result})
        else:
            self.return_json({'result':'100000'})

    def get(self):
        pass


class ConfirmPasswordHandler(UserHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        password=self.get_argument('password')
        if self.confirm_password(uid,password)!=None:
            self.return_json({'result':200})
        else:
            self.return_json({'result':100020,'explain':'password error'})

class LogoutHandler(UserHandler):
    @tornado.web.authenticated
    def get(self):
        uid=self.get_cookie('uid')
        self.logout(uid)
        
class RegHandler(UserHandler):
    def post(self):
        mail=self.get_argument('mail')
        password=self.get_argument('password')
        username=self.get_argument('username')
        self.reg(mail,password,username)

class GetUserInfo(UserHandler):
    def post(self):
        uid=self.get_argument('uid')
        result=self.get_userinfo(uid)
        if result!=None:
            self.return_json({'result':200,'userinfo':result})
        else:
            self.return_json({'result':100021,'explain':'error,getuserinfo'})

    def get(self):
        uid=self.get_cookie('uid')
        result=self.get_userinfo(uid)
        if result!=None:
            self.return_json({'result':200,'userinfo':result})
        else:
            self.return_json({'result':100021,'explain':'error,getuserinfo'})

class UpdateUserHandler(UserHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        username=self.get_argument('username') 
        userinfo=self.get_argument('info')
        clear_time=self.get_argument('clear_time')
        now_pid=self.get_argument('nowpid')
        try:
            password=self.get_argument('password')
            password=Safe.md5(password)
            if self.update_one('user',{'uid':uid},name=username,password=password)==None:
                self.return_json({'result':100017,'explain':'update user error'})
                return None
        except:
            if self.update_one('userinfo',{'uid':uid},name=username,info=userinfo,clear_time=clear_time,nowpid=now_pid)!=None:
                self.return_json({'result':200})
            else:
                self.return_json({'result':100017,'explain':'update user error'})
                return None
