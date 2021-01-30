# -*- coding: utf-8 -*-
import frida
import sys

# HOOK 二进制数与字符串的转换
jscode = """
Java.perform(function () {
    var login = Java.use('com.qianyu.helloworld.LoginActivity$1');
    var Arrays = Java.use("java.util.Arrays");//获取java.util.Arrays类
    login.onClick.implementation = function (a) {
        send("Hook Start...");

        var bytes = stringToBytes("yi jin jiao yu!")
        send(bytes);

        var str = bytesToString(bytes)
        send(str);
        
        var paramStr1 = bytes2HexString(param);
        console.log('param hex : \\n' + paramStr1);

        //以字符串的形式 打印 byte[] 数组
        var bytesStr = Arrays.toString(bytes);
        console.log('bytesStr : ' + bytesStr);
    }

    //字符串转byte[]数组
    function stringToBytes(str) {
        var ch, st, re = [];
        for (var i = 0; i < str.length; i++) {
            ch = str.charCodeAt(i);
            st = [];
            do {
                st.push(ch & 0xFF);
                ch = ch >> 8;
            }
            while (ch);
            re = re.concat(st.reverse());
        }
        return re;
    }

    //byte[]数组转字符串
    function bytesToString(arr) {
        if (typeof arr === 'string') {
            return arr;
        }
        var str = '',
            _arr = arr;
        for (var i = 0; i < _arr.length; i++) {
            var one = _arr[i].toString(2), v = one.match(/^1+?(?=0)/);
            if (v && one.length == 8) {
                var bytesLength = v[0].length;
                var store = _arr[i].toString(2).slice(7 - bytesLength);
                for (var st = 1; st < bytesLength; st++) {
                    store += _arr[st + i].toString(2).slice(2);
                }
                str += String.fromCharCode(parseInt(store, 2));
                i += bytesLength - 1;
            } else {
                str += String.fromCharCode(_arr[i]);
            }
        }
        return str;
    }
    
    //byte[]数组转字符串,或打印出来
    function bytesToString2(x) {
        if (typeof arr === 'string') {
            return arr;
        }
        var arr = Java.use("java.util.Arrays");
        var JavaString = Java.use("java.lang.String");
        send("参数对应数组:" + arr.toString(x))
        send("参数对应字符串:" + JavaString.$new(x))
    }
    
    //byte数组转十六进制字符串，对负值填坑
    function bytes2HexString(arrBytes) {
        var str = "";
        for (var i = 0; i < arrBytes.length; i++) {
            var tmp;
            var num = arrBytes[i];
            if (num < 0) {
                //此处填坑，当byte因为符合位导致数值为负时候，需要对数据进行处理
                tmp = (255 + num + 1).toString(16);
            } else {
                tmp = num.toString(16);
            }
            if (tmp.length == 1) {
                tmp = "0" + tmp;
            }
            str += tmp;
        }
        return str;
    }

});
"""


def message(message, data):
    if message["type"] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


process = frida.get_remote_device().attach('com.qianyu.helloworld')
script = process.create_script(jscode)
script.on("message", message)
script.load()
sys.stdin.read()
