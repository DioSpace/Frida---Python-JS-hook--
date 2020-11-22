# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 03:58:39 2020

@author: Dio
"""

import frida
import sys

# HOOK普通方法 (除了不指定参数类型外,跟hook Overload重载方法写法一样)
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.my.fridademo.Util");//获取到类
        util.ordinaryFunc.implementation = function(param1, param2, param3){
            //打印堆栈
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            console.log("Hook Start...");
    		send(arguments[0]);
            send(arguments[1]);
            send(arguments[2]);
            var handleParam = arguments[0] + arguments[1];
    		send(handleParam);
            return "Hooked 后: 成功hook住";
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
