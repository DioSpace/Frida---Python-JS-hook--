# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 15:52:36 2020

@author: Dio
"""

import frida, sys

#HOOK navtive方法(就跟hook普通方法是一样的)
jscode = """
if(Java.available){
    Java.perform(function(){
        var mainActivity = Java.use("com.my.fridademo.MainActivity");//获取到类
        mainActivity.getString.implementation = function(){
            return "Hooked: hook住 native function";
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