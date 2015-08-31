# Entertainment_and_learning

idea come from http://www.zhihu.com/question/33453309#answer-19211320

going on....


/reg /login
(mail,password)其中密码以明文发送

/logout
(无参数)

/addtask
(library,taskname,taskinfo,score,[limit])
其中limit为可选,不填则为-1(即不限次数)

/updatetask
(library,taskname,taskinfo,score,[limit])
其中limit为可选,不填则为-1(即不限次数)

/deltask
(tid)

/compeletetask
(tid)

/addproject
(projectname,info)

/updateproject
(pid,projectname,info)

/delproject
(pid)
注意:只能删除当前登陆账号所拥有的project,否则返回错误

/shareproject
(pid)
注意:只能分享当前登陆账号所拥有的project,否则返回错误

/unshareproject
(pid)
注意:只能分享当前登陆账号所拥有的project,否则返回错误
