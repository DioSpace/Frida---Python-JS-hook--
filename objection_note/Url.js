//Url 的初始化方法
if(Java.available){
    Java.perform(function(){
        var Classz = Java.use("java.net.URL");
        Classz.$init.overload("java.lang.String").implementation=function(param1){
            console.log(param1);
            this.$init(param1);
        }
    });
}