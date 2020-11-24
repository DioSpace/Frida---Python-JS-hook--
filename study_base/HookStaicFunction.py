# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 13:41:24 2020

@author: Dio
"""

import frida, sys

#HOOK 静态方法 (其实就跟普通方法一样)
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.my.fridademo.Util");//获取到类
        util.myInfo.implementation = function(param1, param2){
            console.log(param1);
            console.log(param2);
            return "Hooked 后: 你们都很优秀";
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