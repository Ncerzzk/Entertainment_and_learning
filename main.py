#!/usr/bin/env python
# encoding: utf-8

import time
import hashlib
import json
import re
import pymysql
import tornado.ioloop
import tornado.web

class Safe(object):
    @staticmethod
    def clear(string):
        """
        prevent from sql attack
        """
        r='select|insert|update|delete|drop|into'
        pattern=re.compile(r)
        try:
            string=string.decode('utf-8')
        except:
            pass
        result=re.sub(pattern,'',string)
        return result

    @staticmethod
    def md5(string):
        m=hashlib.md5()
        m.update(string.encode())
        return m.hexdigest()

    @staticmethod
    def get_time():
        return int(time.time())

    @staticmethod
    def get_session(salt):
        t=str(Safe.get_time())
        string=t+str(salt)
        return Safe.md5(string)
    
    @staticmethod
    def get_deadline(days=30):
        t=Safe.get_time()
        t+=24*60*60*days
        return t

class DB(object):
    def __init__(self,host,user,password,db,charset='utf8'):
        self.conn=pymysql.connect(host=host,user=user,passwd=password,db=db,charset=charset)
        self.cur=self.conn.cursor()

    def insert(self,table,dic):
        """
         dic is a dictionary like:
         {
         'username':hello,
         'password':1234567
         }
        """
        key=''
        value=''
        for i in dic:
            key+=i+','
            value+='\''+Safe.clear(str(dic[i]))+'\''+','
        key=key[:-1:]
        value=value[:-1:]
        sql='insert into %s(%s) values(%s);' %(table,key,value)
        stats=self.cur.execute(sql)
        self.conn.commit()
        if stats==0:
            print("error,happened when insert into table.")
            return 1

    @staticmethod
    def deal_condition(condition):
        result=''
        for i in condition:
            result+=i+'=\''+Safe.clear(str(condition[i]))+'\' and '
        return result[:-4:]

    def del_one(self,table,condition):
        """
        condition is a dict like {'uid':1}
        """
        sql='delete from %s where ' % table
        condition=DB.deal_condition(condition)
        sql+=condition+';'
        stats=self.cur.execute(sql)
        self.conn.commit()
        if stats==0:
            print("error,happened when del_one")
            return 1
      
    
    def update(self,table,value,condition):
        condition=DB.deal_condition(condition)
        value=DB.deal_condition(value)
        value=value.replace('and',',')
        sql='update %s set %s where %s;' % (table,value,condition)
        stats=self.cur.execute(sql)
        self.conn.commit()
        if stats==0:
            print("error,happened when update")
            return 1
    def select(self,table,condition):
        """
        found,return the list;
        else,return 1;
        """
        condition=DB.deal_condition(condition)
        sql='select * from %s where %s;' % (table,condition)
        stats=self.cur.execute(sql)
        if stats==0:
            print("error,nothing found,happened when select")
            return 1
        else:
            return list(self.cur)

    def __del__(self):
        self.cur.close()
        self.conn.close()

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db=DB('localhost','root','6789mm','learning')


    def return_json(self,obj):
        self.set_header('Content-type','application/json')
        self.write(json.dumps(obj))

    def get_current_user(self):
        uid=self.get_cookie('uid')
        session=self.get_cookie('session')
        username=self.get_cookie('username')
        if uid==None:
            return None
        result=self.db.select('session',{'uid':uid,'session':session})[0]
        if result!=1:
            now_time=Safe.get_time()
            if int(now_time)>int(result[3]):
                """
                out time
                """
                return None
            else:
                return username
        else:
            return None

class LoginHandler(BaseHandler):
    def post(self):
        mail=self.get_argument('mail')
        password=self.get_argument('pwd')
        password=Safe.md5(password)
        result = self.db.select('user',{'mail':mail,'password':password})[0]
        username=result[1]
        uid=result[0]
        if result!=1:
            """
            login success,check session;
            """
            sessionresult=self.db.select('session',{'uid':uid})
            now_time=Safe.get_time()
            if sessionresult==1:
                "never logined before"
                deadline=Safe.get_deadline()
                session=Safe.get_session(mail)
                self.db.insert('session',{'uid':uid,'session':session,'deadline':deadline})
            else:    
                deadline=sessionresult[0][3]
                session=sessionresult[0][2]
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
            print("login success and set cookie yet")


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        pid=self.get_argument('pid')
        if self.db.del_one('session',{'uid':uid})!=1:
            self.return_json({'result':200})
            print("logout success")
        else:
            print("error,when logout")

        self.clear_all_cookies()


            
class TestHandler(BaseHandler):
    def post(self):
        self.db.del_one('task',{'uid':1})
                
class RegHandler(BaseHandler):
    def post(self):
        mail=self.get_argument('mail')
        password=self.get_argument('pwd')
        password=Safe.md5(password)
        """
        rember to clear evil code in mail and password.
        """
        if self.db.select('user',{'mail':mail})!=1:
            # existed user
            self.return_json({'result':100001,'explain':'the user has signed.'})
            print('user has signed.')
            return 1
        if self.db.insert('user',{'mail':mail,'password':password})!=1:
            result=self.db.select('user',{'mail':mail})[0]
            uid=result[0]
            session=Safe.get_session(mail)
            deadline=Safe.get_deadline()
            self.db.insert('session',{'uid':uid,'session':session,'deadline':deadline})
            self.return_json({'result':200,'uid':uid,'session':session})


            self.set_cookie('uid',str(uid))
            self.set_cookie('session',session)
            print('reg success')
            """
            reg success,return session.
            return json.
            """
        else:
            print("error,when regging")
        
        
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
            print('add_task success')
            result = {
                'result':200
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
        result=self.db.del_one('task',{'uid':uid,'tid':tid})
        if result==1:
            self.return_json({'result':100003,'explain':'task not found'})
            return None
        else:
            self.return_json({'result':200})
        



class CompeleteTaskHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid=self.get_cookie('uid')
        tid=self.get_argument('tid')
        result=self.db.select('task',{'tid':tid})
        if result==1:
            self.return_json({'result':100003,'explain':'task not found'})
            return 1
        if result[0][8]!=0:
            time=int(result[0][8])
            score=int(result[0][3])
            userinfo=self.db.select('user',{'id':uid})
            todayscore=int(userinfo[0][6])+score
            try:
                self.db.update('user',{'today_score':todayscore},{'id':uid}) 
                self.db.update('task',{'time_remain':time-1},{'tid':tid})
            except:
                return None
            print("compeletetask sucess")
            self.return_json({'result':200})
        else:
            print("error,happened when compeletetask")
            self.return_json({'result':100002,'explain':'time_remain is 0'})
            return None


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
            print("add project success")
            self.return_json({'result':200})
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
        if self.db.del_one('project',{'owner_id':uid,'pid':pid})!=1:
            self.return_json({'result':200})
            print('del_project success')
        else:
            self.return_json({'result':100005,'explain':'del_project error'})
            print('error,del_project')
            return None

      

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

class UserInfoHandler(BaseHandler):
    def post(self):
        pass

class UpdateUserInfoHandler(BaseHandler):
    def post(self):
        pass 
"""
a=DB('localhost','root','6789mm','learning')
# a.insert('user',{'name':'hello','password':'1234' })
a.del_one('user',{'name':'hello'})
print(a.select('user',{'id':5}))
"""

application = tornado.web.Application([
        (r"/test",TestHandler),
        (r"/reg", RegHandler),
        (r"/login",LoginHandler),
        (r"/logout",LogoutHandler),
        (r"/addtask",AddTaskHandler),
        (r"/updatetask",UpdateTaskHandler),
        (r"/deltask",DelTaskHandler),
        (r"/compeletetask",CompeleteTaskHandler),
        (r"/addproject",AddProjectHandler),
        (r"/delproject",DelProjectHandler),
        (r"/updateproject",UpdateProjectHandler),
        (r"/shareproject",ShareProjectHandler),
        (r"/unshareproject",UnShareProjectHandler)

])

application.listen(8888)
tornado.ioloop.IOLoop.instance().start()
