#!/bin/bash
ca=$1
device_id=$2

hash=$(openssl x509 -inform PEM -subject_hash_old -in $ca| head -1)
cert_name=$hash.0

adb -s $device_id root
adb -s $device_id remount
adb -s $device_id push $ca /system/etc/security/cacerts/$cert_name
adb -s $device_id reboot