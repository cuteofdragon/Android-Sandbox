function fileHooks(){
    const File = Java.use("java.io.File")
    constructor = [
        File.$init.overload("java.lang.String"),
        File.$init.overload("java.lang.String", "java.lang.String")
    ]

    constructor[0].implementation = function(a0) {
        send("file: " + a0);
        var ret = constructor[0].call(this,a0);
        return ret;
    }

   constructor[1] = function(a0, a1) {
        send("file: " + a0 + "/" + a1);
        var ret = constructor[1].call(this,a0,a1);
        return ret;
    }
}

fileHooks()