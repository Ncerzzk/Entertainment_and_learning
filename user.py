#!/usr/bin/env python
# coding=utf-8
from base import *
from safe import *

class UserHandler(BaseHandler):
    def add_user(self,mail,password): 
        password=Safe.md5(password)
        if self.db.insert('user',{'mail':mail,'password':password})!=1:
            uid=self.db.get_id()
            self.db.insert('userinfo',{'uid':uid})
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
        result = self.db.select('user',{'mail':mail,'password':password},'name,uid')[0]
        username=result['name']
        uid=result['uid']
        if result!=1:
            """
            login success,check session;
            """
            sessionresult=self.db.select('session',{'uid':uid},'session,deadline')
            now_time=Safe.get_time()
            if sessionresult==1:
                "never logined before"
                deadline=Safe.get_deadline()
                session=Safe.get_session(mail)
                self.add_session(uid,session,deadline)
            else:    
                deadline=sessionresult[0]['deadline']
                session=sessionresult[0]['session']
                if int(now_time)>int(deadline):
                    session=Safe.get_session(mail)
                    new_deadline=Safe.get_deadline()
                    """
                    update the session
                    """
                    self.update_one('session',{'uid':uid},session=session,deadline=new_deadline)

            self.set_cookie('uid',str(uid))
            username=username or 'null'
            self.set_cookie('username',username)
            self.set_cookie('session',session)
            self.return_json({'result':200,'uid':uid,'session':session})
            print("login success and set cookie yet")

    def logout(self,uid):
        if self.db.del_one('session',{'uid':uid})!=1:
            self.return_json({'result':200})
            print("logout success")
        else:
            print("error,when logout")

        self.clear_all_cookies()

    def reg(self,mail,password):
        try:
            username=self.get_argument('username')
        except:
            username='null'
        """
        rember to clear evil code in mail and password.
        """
        if self.db.select('user',{'mail':mail},'uid')!=1:
            # existed user
            self.return_json({'result':100001,'explain':'the user has signed.'})
            print('user has signed.')
            return None
        uid=self.add_user(mail,password)
        if uid !=None:
            session=Safe.get_session(mail)
            deadline=Safe.get_deadline()
            self.add_session(uid,session,deadline)
            self.return_json({'result':200,'uid':uid,'session':session})
            self.set_cookie('username',username)
            self.set_cookie('uid',str(uid))
            self.set_cookie('session',session)
            print('reg success')
            """
            reg success,return session.
            return json.
            """
        else:
            print("error,when regging")
        

class LoginHandler(UserHandler):
    def post(self):
        mail=self.get_argument('mail')
        password=self.get_argument('password')
        self.login(mail,password)
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
        self.reg(mail,password)

class GetUserInfo(UserHandler):
    def post(self):
        uid=self.get_argument('uid')
        self.get_info('userinfo',uid)

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
