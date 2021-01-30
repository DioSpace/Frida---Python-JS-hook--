# -*- coding: utf-8 -*-

import frida
import sys

# 获取证书对应的密码
# [B ---> byte[] ,  [C  ---> char[]
jscode = """
if(Java.available){
    Java.perform(function(){
        var Singleton = Java.use("java.security.KeyStore");//获取到类
        //var util = Singleton.getInstance("PKCS12");//调用单例方法初始化一个对象
        Singleton.load.overload("java.io.InputStream","[C").implementation = function(param1, param2){
            console.log("Hook Start...");
            if(param2 != null){
                var JavaString = Java.use("java.lang.String");
                send("param2:" + JavaString.$new(param2));
            }
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
session = frida.get_usb_device().attach('com.myself.network')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
