function replaceFinaleField(object, fieldName, value){
    var field =  object.class.getDeclaredField(fieldName)
    field.setAccessible(true)
    field.set(null, value)
}

function bypass_build_properties(){
        // Class containing const that we want to modify
        const Build = Java.use("android.os.Build")

        // reflection class for changing const
        const Field = Java.use('java.lang.reflect.Field')
        const Class = Java.use('java.lang.Class')

        // Replacing Build static fields
        replaceFinaleField(Build, "FINGERPRINT", "abcd/C1505:4.1.1/11.3.A.2.13:user/release-keys")
        replaceFinaleField(Build, "MODEL", "C1505")
        replaceFinaleField(Build, "MANUFACTURER", "Sony")
        replaceFinaleField(Build, "BRAND", "Xperia")
        replaceFinaleField(Build, "BOARD", "7x27")
        replaceFinaleField(Build, "ID", "11.3.A.2.13")
        replaceFinaleField(Build, "SERIAL", "abcdef123")
        replaceFinaleField(Build, "TAGS", "release-keys")
        replaceFinaleField(Build, "USER", "administrator")
}

function bypass_phonenumber(){
    const TelephonyManager = Java.use('android.telephony.TelephonyManager')
    TelephonyManager.getLine1Number.overload().implementation = function(){
        console.log("Phone number bypass")
        return "060102030405"
    }
}

function bypass_deviceid(){
    const TelephonyManager = Java.use('android.telephony.TelephonyManager')
    TelephonyManager.getDeviceId.overload().implementation = function(){
        console.log("Device id")
        return "012343545456445"
    }
}

function bypass_imsi(){
    const TelephonyManager = Java.use('android.telephony.TelephonyManager')
    TelephonyManager.getSubscriberId.overload().implementation = function(){
        console.log("Suscriber ID")
        return "310260000000111"
    }
}

function bypass_operator_name(){
    const TelephonyManager = Java.use('android.telephony.TelephonyManager')
    TelephonyManager.getNetworkOperatorName.overload().implementation = function(){
        console.log("Operator Name")
        return "not"
    }
}

function bypass_sim_operator_name(){
    const TelephonyManager = Java.use('android.telephony.TelephonyManager')
    TelephonyManager.getSimOperatorName.overload().implementation = function(){
        console.log("Operator Name")
        return "not"
    }
}

function bypass_has_file(){
    const File = Java.use("java.io.File")
    const KnownFiles= [
        "ueventd.android_x86.rc",
        "x86.prop",
        "ueventd.ttVM_x86.rc",
         "init.ttVM_x86.rc",
        "fstab.ttVM_x86",
        "fstab.vbox86",
        "init.vbox86.rc",
        "ueventd.vbox86.rc",
        "/dev/socket/qemud",
        "/dev/qemu_pipe",
        "/system/lib/libc_malloc_debug_qemu.so",
        "/sys/qemu_trace",
        "/system/bin/qemu-props",
        "/dev/socket/genyd",
        "/dev/socket/baseband_genyd",
        "/proc/tty/drivers",
        "/proc/cpuinfo"
    ]

   
        File.exists.implementation = function () {
          var x = this.getAbsolutePath();
          for(var i=0; i<KnownFiles.length; i++){
            
            if(KnownFiles[i] == x){
              return false;
            }
          }
      
          return this.exists();
        };
}

function bypass_processbuilder(){
    var ProcessBuilder = Java.use('java.lang.ProcessBuilder');

    ProcessBuilder.$init.overload('[Ljava.lang.String;').implementation = function(x){
        console.log("ProcessBuilder")
        return null
    }
}


function bypass_system_properties() {
    /*
    * Function used to bypass common checks to
    * Android OS properties
    * Bypass the props checking from this git : https://github.com/strazzere/anti-emulator
    *
    */
    const SystemProperties = Java.use('android.os.SystemProperties')
    const String = Java.use('java.lang.String')
    const Properties = {
        "init.svc.qemud": null,
        "init.svc.qemu-props": null,
        "qemu.hw.mainkeys": null,
        "qemu.sf.fake_camera": null,
        "qemu.sf.lcd_density": null,
        "ro.bootloader": "xxxxx",
        "ro.bootmode": "xxxxxx",
        "ro.hardware": "xxxxxx",
        "ro.kernel.android.qemud": null,
        "ro.kernel.qemu.gles": null,
        "ro.kernel.qemu": "xxxxxx",
        "ro.product.device": "xxxxx",
        "ro.product.model": "xxxxxx",
        "ro.product.name": "xxxxxx",
        "ro.serialno": null
    }

    SystemProperties.get.overload('java.lang.String').implementation = function(x){
        console.log("Property " + x)

        if (x in Properties){
            console.log('Returning ' + Properties[x])
            return Properties[x]
        }
        return this.get(x)
    }

}

exports.bypass_build_properties = bypass_build_properties
exports.bypass_phonenumber = bypass_phonenumber
exports.bypass_deviceid = bypass_deviceid
exports.bypass_imsi = bypass_imsi
exports.bypass_operator_name = bypass_operator_name
exports.bypass_sim_operator_name = bypass_sim_operator_name
exports.bypass_has_file = bypass_has_file
exports.bypass_processbuilder = bypass_processbuilder
exports.bypass_system_properties = bypass_build_properties
