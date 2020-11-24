# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 03:46:25 2020

@author: Dio
"""

import frida, sys
#HOOK so 文件
jscode = """
setImmediate(function () {
    send("start");
    //遍历模块找基址
    Process.enumerateModules({
        onMatch: function (exp) {
            if (exp.name == 'libnative-lib.so') {
                send('enumerateModules find');
                send(exp.name + "|" + exp.base + "|" + exp.size + "|" + exp.path);
                send(exp);
                return 'stop';
            }
        },
        onComplete: function () {
            send('enumerateModules stop');
        }
    });
    
    //hook导出函数
    var exports = Module.enumerateExportsSync("libnative-lib.so");
    for(var i=0;i<exports.length;i++){
        send("name:"+exports[i].name+"  address:"+exports[i].address);
    }
    
    //通过模块名直接查找基址
    var baseSOFile = Module.findBaseAddress("libnative-lib.so");
    Interceptor.attach(baseSOFile.add(0x00009527),{
        onEnter: function(args) {
            console.log("base address");
            //console.log(Memory.readCString(args[0]));
            //console.log(Memory.readUtf16String(args[3]));
            console.log(args[2]);
            //console.log(args[3]);
            //console.log(args[4]);
        },
        onLeave: function(retval){
            //打印原返回值
            console.log("返回值:"+retval);
            //替换返回值
            retval.replace(3);
        }
    });
});
"""

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

process = frida.get_usb_device().attach('com.my.fridademo')
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()
