//主动调用
Java.perform(function(){
    var Util2 = Java.use("com.my.fridademo.Util2");//获取到类
    //静态成员变量可以直接设置结果
    Util2.static_bool_var.value = true;//改变静态属性值
    console.log("After set new value 1:" + Util2.static_bool_var.value);
    Util2.active_static_call_func("param_hooked");
});