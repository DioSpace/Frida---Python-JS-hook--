# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 19:49:55 2020

@author: Dio
"""

import frida
import sys

#HOOK重载方法(根据传入参数的个数和类型来区分方法名相同的函数)
jscode = """
/* 这个字段标记Java虚拟机（例如： Dalvik 或者 ART）是否已加载, 操作Java任何东西的之前，要确认这个值是否为true */
if(Java.available){
    /* 111、222、333 打这些log的目的是看流程走到哪里 */
    console.log("111");
    
    /* Java.perform(function(){ ... Javascript代码成功被附加到目标进程时调用，我们核心的代码要在里面写。是个固定格式 */
    Java.perform(function(){
        
        /* Java.use方法用于声明一个Java类，在用一个Java类之前首先得声明。比如声明一个String类，要指定完整的类名var StringClass=Java.use("java.lang.String"); */
        var util = Java.use("com.my.fridademo.Util");
        console.log("222");
        
        /* 类.函数.overload(参数类型).implementation = function(形参名称){ */
        util.judgeByAge.overload("int").implementation = function(age){
            console.log("333");
            
            /* 给judgeByAge函数传参、得到addnumber函数的返回值 */
            console.log(this.judgeByAge(88));
            
            /* 修改judgeByAge函数的返回值 */
            return "hooked: 永远年轻";
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