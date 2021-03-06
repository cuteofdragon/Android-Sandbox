import logging
import os

current_path = os.path.dirname(os.path.realpath(__file__))

def onload():
    logging.debug("Example:loaded()")

def onunload():
    logging.debug("Example:unloaded()")

def parse(module,message):
    logging.debug("Example:parse()")

def get_frida_script():
    logging.debug("Example:get_frida_script()")
    with open(f"{current_path}/frida.js") as f:
        return ("Example", f.read())