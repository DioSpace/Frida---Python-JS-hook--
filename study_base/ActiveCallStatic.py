# -*- coding: utf-8 -*-
import frida, sys

# HOOK 主动调用静态方法
jscode = """
if(Java.available){
    Java.perform(function(){
        var Util2 = Java.use("com.my.fridademo.Util2");//获取到类
        //静态成员变量可以直接设置结果
        Util2.static_bool_var.value = true;//改变静态属性值
        console.log("After set new value 1:" + Util2.static_bool_var.value);
        Util2.active_static_call_func("param_hooked");
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
