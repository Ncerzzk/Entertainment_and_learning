# Entertainment_and_learning

idea come from http://www.zhihu.com/question/33453309#answer-19211320


/user/reg  (mail,password)其中密码以明文发送 method=POST
/user/login (mail,password)其中密码以明文发送 method=POST
/user/logout method=GET 无参数
/user/update (username,info,clear_time,nowpid,[password]) method=POST
密码为可选,若不修改,请不要带上.

/task/add method=POST
(library,taskname,taskinfo,score,[limit])
其中limit为可选,不填则为-1(即不限次数)

/task/update method=POST
(tid,library,taskname,taskinfo,score,[limit])
其中limit为可选,不填则为-1(即不限次数)

/task/del method=POST
(tid)

/task/compelete method=POST
(tid)

/task/get  method=POST (获取任务信息)
(tid)

/task/getlibrary method=GET (获取当前project的分库名称)

/task/getnowtask method=GET (获取当前project的任务)

/project/add   method=POST
(projectname,info)  

/project/setnowpid method=POST (设置当前用户的当前project)
(pid)

/project/update method=POST
(pid,projectname,info)

/project/del method=POST
(pid)
注意:只能删除当前登陆账号所拥有的project,否则返回错误

/project/share method=POST
(pid)
注意:只能分享当前登陆账号所拥有的project,否则返回错误

/project/unsharemethod=POST 
(pid)
注意:只能分享当前登陆账号所拥有的project,否则返回错误

/project/change(建议用这个代替share和unshare) method=POST
(pid)
注意:只能分享当前登陆账号所拥有的project,否则返回错误

/project/get (获取project信息) method=POST
(pid)

/project/getall (获取当前用户所有project) method=GET

