# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 22:04:13 2020

@author: Dio
"""

import frida, sys

#HOOK构造方法
jscode = """
if(Java.available){
    Java.perform(function(){
        var student = Java.use("com.my.fridademo.Student");
        student.$init.overload("java.lang.String","java.lang.String","int","double","boolean").implementation=function(param1,param2,param3,param4,param5){
            console.log(param1);
            console.log(param2);
            console.log(param3);
            console.log(param4);
            console.log(param5);
            this.$init("Leo","man",18,99.5,true);
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