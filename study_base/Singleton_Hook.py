# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 13:41:26 2020

@author: Dio
"""

import frida, sys

#hook单例里的方法
jscode = """
if(Java.available){
    Java.perform(function(){
        var Singleton = Java.use("com.my.fridademo.MySingleton");//获取到类
        var util = Singleton.getInstance();//调用单例方法初始化一个对象
        util.post.overload("java.lang.String").implementation = function(param){
            var result = this.post(param);
            console.log("param : " + param);
            return result + " ---> hooked";
        }
    });
}
"""

def on_message(message, data):
    if message['type'] == 'send':
        print(" {0}".format(message['payload']))
    else:
        print(message)

# 查找USB设备并附加到目标进程
session = frida.get_usb_device().attach('com.my.fridademo')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()