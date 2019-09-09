# Android Malware Sandbox

This project aim to provide a simple configurable and modulable sandbox for quickly sandbox known or unknown families of
Android Malware.

## Requirements

An emulator created with AVD would be the best, I personnaly use an AVD emulator with Android 7.0 without Google Apis and Arch:x86_64.

```
pip install -r requirements.txt
sudo npm install -g frida-compile
npm install
```

## Usage :

```
python3 main.py <file(s) to analyse>
```

## How it works

This sandbox is tested on Android 7 emulator.

It will spawn an emulator and then install the necessary to use Frida, then spawn a Mitmproxy install and install it's certificate.
Then it will install all the applications one by one and log all their behaviours ( depending on your config ).

To configure your analysis, the config file is located in `config/config.ini` 

## Customizing

You can easily add a plugin in plugins folder to automatically hook calls, and then save them to the database


## TODO(s) :
* Improve reports
