#!/usr/bin/env python
# coding=utf-8
from base import *
from safe import *

class LoginHandler(BaseHandler):
    def post(self):
        mail=self.get_argument('mail')
        password=self.get_argument('password')
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
                self.db.insert('session',{'uid':uid,'session':session,'deadline':deadline})
            else:    
                deadline=sessionresult[0]['deadline']
                session=sessionresult[0]['session']
                if int(now_time)>int(deadline):
                    session=Safe.get_session(mail)
                    new_deadline=Safe.get_deadline()
                    """
                    update the session
                    """
                    self.db.update('session',{'session':session,'uid':uid,'deadline':new_deadline},{'uid'})

            self.set_cookie('uid',str(uid))
            username=username or 'null'
            self.set_cookie('username',username)
            self.set_cookie('session',session)
            self.return_json({'result':200,'uid':uid,'session':session})
            print("login success and set cookie yet")


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        if self.db.del_one('session',{'uid':uid})!=1:
            self.return_json({'result':200})
            print("logout success")
        else:
            print("error,when logout")

        self.clear_all_cookies()

class RegHandler(BaseHandler):
    def post(self):
        mail=self.get_argument('mail')
        password=self.get_argument('password')
        password=Safe.md5(password)
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
        if self.db.insert('user',{'mail':mail,'password':password})!=1:
            uid=self.db.get_id()
            self.db.insert('userinfo',{'uid':uid})
            session=Safe.get_session(mail)
            deadline=Safe.get_deadline()
            self.db.insert('session',{'uid':uid,'session':session,'deadline':deadline})
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
        
class GetUserInfo(BaseHandler):
    def post(self):
        uid=self.get_argument('uid')
        self.get_info('userinfo',uid)
