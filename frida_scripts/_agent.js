(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";

var proxy_hooks = require('./lib/proxy_hooks.js');

var hooks = require('./lib/hooks.js');

var anti_emulator = require('./lib/anti-emulator.js');

Java.perform(function () {
  anti_emulator.bypass_build_properties();
  anti_emulator.bypass_phonenumber();
  anti_emulator.bypass_deviceid();
  anti_emulator.bypass_imsi();
  anti_emulator.bypass_operator_name();
  anti_emulator.bypass_sim_operator_name();
  anti_emulator.bypass_has_file();
  anti_emulator.bypass_processbuilder();
  anti_emulator.bypass_system_properties();
  hooks.to_string();
  hooks.url_init();
  hooks.dexclass_loader();
  proxy_hooks.bypass_ssl_pinning();
});

},{"./lib/anti-emulator.js":2,"./lib/hooks.js":3,"./lib/proxy_hooks.js":4}],2:[function(require,module,exports){
"use strict";

function replaceFinaleField(object, fieldName, value) {
  var field = object["class"].getDeclaredField(fieldName);
  field.setAccessible(true);
  field.set(null, value);
}

function bypass_build_properties() {
  // Class containing const that we want to modify
  var Build = Java.use("android.os.Build"); // reflection class for changing const

  var Field = Java.use('java.lang.reflect.Field');
  var Class = Java.use('java.lang.Class'); // Replacing Build static fields

  replaceFinaleField(Build, "FINGERPRINT", "abcd/C1505:4.1.1/11.3.A.2.13:user/release-keys");
  replaceFinaleField(Build, "MODEL", "C1505");
  replaceFinaleField(Build, "MANUFACTURER", "Sony");
  replaceFinaleField(Build, "BRAND", "Xperia");
  replaceFinaleField(Build, "BOARD", "7x27");
  replaceFinaleField(Build, "ID", "11.3.A.2.13");
  replaceFinaleField(Build, "SERIAL", "abcdef123");
  replaceFinaleField(Build, "TAGS", "release-keys");
  replaceFinaleField(Build, "USER", "administrator");
}

function bypass_phonenumber() {
  var TelephonyManager = Java.use('android.telephony.TelephonyManager');

  TelephonyManager.getLine1Number.overload().implementation = function () {
    console.log("Phone number bypass");
    return "060102030405";
  };
}

function bypass_deviceid() {
  var TelephonyManager = Java.use('android.telephony.TelephonyManager');

  TelephonyManager.getDeviceId.overload().implementation = function () {
    console.log("Device id");
    return "012343545456445";
  };
}

function bypass_imsi() {
  var TelephonyManager = Java.use('android.telephony.TelephonyManager');

  TelephonyManager.getSubscriberId.overload().implementation = function () {
    console.log("Suscriber ID");
    return "310260000000111";
  };
}

function bypass_operator_name() {
  var TelephonyManager = Java.use('android.telephony.TelephonyManager');

  TelephonyManager.getNetworkOperatorName.overload().implementation = function () {
    console.log("Operator Name");
    return "not";
  };
}

function bypass_sim_operator_name() {
  var TelephonyManager = Java.use('android.telephony.TelephonyManager');

  TelephonyManager.getSimOperatorName.overload().implementation = function () {
    console.log("Operator Name");
    return "not";
  };
}

function bypass_has_file() {
  var File = Java.use("java.io.File");
  var KnownFiles = ["ueventd.android_x86.rc", "x86.prop", "ueventd.ttVM_x86.rc", "init.ttVM_x86.rc", "fstab.ttVM_x86", "fstab.vbox86", "init.vbox86.rc", "ueventd.vbox86.rc", "/dev/socket/qemud", "/dev/qemu_pipe", "/system/lib/libc_malloc_debug_qemu.so", "/sys/qemu_trace", "/system/bin/qemu-props", "/dev/socket/genyd", "/dev/socket/baseband_genyd", "/proc/tty/drivers", "/proc/cpuinfo"];

  File.$init.overload('java.lang.String').implementation = function (x) {
    if (x in KnownFiles) {
      console.log(x);
      return null;
    }

    return this.$init(x);
  };
}

function bypass_processbuilder() {
  var ProcessBuilder = Java.use('java.lang.ProcessBuilder');

  ProcessBuilder.$init.overload('[Ljava.lang.String;').implementation = function (x) {
    console.log("ProcessBuilder");
    return null;
  };
}

function bypass_system_properties() {
  /*
  * Function used to bypass common checks to
  * Android OS properties
  * Bypass the props checking from this git : https://github.com/strazzere/anti-emulator
  *
  */
  var SystemProperties = Java.use('android.os.SystemProperties');
  var String = Java.use('java.lang.String');
  var Properties = {
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
  };

  SystemProperties.get.overload('java.lang.String').implementation = function (x) {
    console.log("Property " + x);

    if (x in Properties) {
      console.log('Returning ' + Properties[x]);
      return Properties[x];
    }

    return this.get(x);
  };
}

exports.bypass_build_properties = bypass_build_properties;
exports.bypass_phonenumber = bypass_phonenumber;
exports.bypass_deviceid = bypass_deviceid;
exports.bypass_imsi = bypass_imsi;
exports.bypass_operator_name = bypass_operator_name;
exports.bypass_sim_operator_name = bypass_sim_operator_name;
exports.bypass_has_file = bypass_has_file;
exports.bypass_processbuilder = bypass_processbuilder;
exports.bypass_system_properties = bypass_build_properties;

},{}],3:[function(require,module,exports){
"use strict";

function url_init() {
  var url = Java.use("java.net.URL");

  url.$init.overload('java.lang.String').implementation = function (var0) {
    if (!var0.startsWith("null")) {
      send("url:" + var0 + "");
    }

    return this.$init(var0);
  };
}

function to_string() {
  var String = Java.use('java.lang.String');

  String.toString.implementation = function () {
    var x = this.toString();

    if (x.length > 5) {
      send("to_string:" + x + "");
    }

    return x;
  };
}

function dexclass_loader() {
  var DexClassLoader = Java.use("dalvik.system.DexClassLoader");

  DexClassLoader.$init.implementation = function (dexPath, optimizedDirectory, librarySearchPath, parent) {
    send("dexclassloader:" + dexPath + "|" + optimizedDirectory + "|" + librarySearchPath + "|" + parent + "");
    this.$init(dexPath, optimizedDirectory, librarySearchPath, parent);
  };
}

exports.to_string = to_string;
exports.dexclass_loader = dexclass_loader;
exports.url_init = url_init;

},{}],4:[function(require,module,exports){
"use strict";

function bypass_ssl_pinning() {
  var array_list = Java.use("java.util.ArrayList");
  var ApiClient = Java.use('com.android.org.conscrypt.TrustManagerImpl');

  ApiClient.checkTrustedRecursive.implementation = function (a1, a2, a3, a4, a5, a6) {
    var k = array_list.$new();
    return k;
  };
}

exports.bypass_ssl_pinning = bypass_ssl_pinning;

},{}]},{},[1])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uLy4uL3Vzci9saWIvbm9kZV9tb2R1bGVzL2ZyaWRhLWNvbXBpbGUvbm9kZV9tb2R1bGVzL2Jyb3dzZXItcGFjay9fcHJlbHVkZS5qcyIsImZyaWRhX3NjcmlwdHMvYWdlbnQuanMiLCJmcmlkYV9zY3JpcHRzL2xpYi9hbnRpLWVtdWxhdG9yLmpzIiwiZnJpZGFfc2NyaXB0cy9saWIvaG9va3MuanMiLCJmcmlkYV9zY3JpcHRzL2xpYi9wcm94eV9ob29rcy5qcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTs7O0FDQUEsSUFBTSxXQUFXLEdBQUcsT0FBTyxDQUFDLHNCQUFELENBQTNCOztBQUNBLElBQU0sS0FBSyxHQUFHLE9BQU8sQ0FBQyxnQkFBRCxDQUFyQjs7QUFDQSxJQUFNLGFBQWEsR0FBRyxPQUFPLENBQUMsd0JBQUQsQ0FBN0I7O0FBQ0EsSUFBSSxDQUFDLE9BQUwsQ0FBYSxZQUFVO0FBQ3RCLEVBQUEsYUFBYSxDQUFDLHVCQUFkO0FBQ0EsRUFBQSxhQUFhLENBQUMsa0JBQWQ7QUFDQSxFQUFBLGFBQWEsQ0FBQyxlQUFkO0FBQ0EsRUFBQSxhQUFhLENBQUMsV0FBZDtBQUNBLEVBQUEsYUFBYSxDQUFDLG9CQUFkO0FBQ0EsRUFBQSxhQUFhLENBQUMsd0JBQWQ7QUFDQSxFQUFBLGFBQWEsQ0FBQyxlQUFkO0FBQ0EsRUFBQSxhQUFhLENBQUMscUJBQWQ7QUFDQSxFQUFBLGFBQWEsQ0FBQyx3QkFBZDtBQUNBLEVBQUEsS0FBSyxDQUFDLFNBQU47QUFDQSxFQUFBLEtBQUssQ0FBQyxRQUFOO0FBQ0EsRUFBQSxLQUFLLENBQUMsZUFBTjtBQUNBLEVBQUEsV0FBVyxDQUFDLGtCQUFaO0FBQ0EsQ0FkRDs7Ozs7QUNIQSxTQUFTLGtCQUFULENBQTRCLE1BQTVCLEVBQW9DLFNBQXBDLEVBQStDLEtBQS9DLEVBQXFEO0FBQ2pELE1BQUksS0FBSyxHQUFJLE1BQU0sU0FBTixDQUFhLGdCQUFiLENBQThCLFNBQTlCLENBQWI7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
