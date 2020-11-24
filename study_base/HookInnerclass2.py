# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:58:48 2020

@author: Dio
"""

import frida, sys

#HOOK 匿名内部类 2 (根据调用方法所在的类,然后找到内部类的序列号来hook,作用域只限这一处)
jscode = """
if(Java.available){
    Java.perform(function(){
        var mainActivity = Java.use("com.my.fridademo.MainActivity$2");//获取到类
        mainActivity.say2.implementation = function(param1){
            console.log("Hook Start...");
            arguments[0] += " hooked 2!";
    		send(arguments[0]); //打印日志
            this.say2(arguments[0]);
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
