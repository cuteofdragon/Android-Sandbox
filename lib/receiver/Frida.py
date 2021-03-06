from lib.receiver.Receiver import Receiver

import subprocess
import logging
import frida
import sys

import os
dirname = os.path.dirname(os.path.realpath(__file__)) + "/../../"

class Frida(Receiver):

    def __init__(self, configuration, module, device):
        Receiver.__init__(self, "FridaReceiver")
        self.configuration = configuration
        self.module = module
        self.device = device

    def start(self):
        '''
        Attach or spawn to an application with Frida
        :return:
        '''
        logging.debug("Frida:start()")

        device = frida.get_device(self.device.device_id)

        spawn = self.configuration.getboolean('spawn_app')

        if (spawn):
            pid = device.spawn([self.module.application.package])
            session = device.attach(pid)
        else:
            pid = device.get_process(self.module.application.package).pid
            session = device.attach(pid)

        self.script = session.create_script(open(f"{dirname}frida_scripts/_agent.js").read())
        self.script.on('message', self.on_message)
        self.script.load()

        if (spawn):
            device.resume(pid)

    def stop(self):
        logging.debug("Frida:stop()")

    def on_message(self, message, data):
        '''
        on message callback used by Frida
        :param message:
        :param data:
        :return:
        '''
        if message['type'] == 'send':
            self.module.parse(message['payload'])
        else:
            print(message)

    @staticmethod
    def compile(configuration,plugin_code = []):
        """
        Function that create the final frida script used by the sandbox
        :return: script_location
        """
        logging.debug("Frida:compile()")

        script = Frida.generate_script(configuration,plugin_code)

        f = open(f"{dirname}frida_scripts/agent.js", "w")
        f.write(script)
        f.close()

        pid = subprocess.Popen(["frida-compile", f"{dirname}frida_scripts/agent.js", "-o", f"{dirname}frida_scripts/_agent.js"],
                               stdout=subprocess.PIPE)
        pid.wait()
        stdout, stderr = pid.communicate()

        if stderr is not None:
            logging.error(f"Error while compiling script : {stderr}")
            sys.exit(-1)
        else:
            logging.info(f'Compiled')

    @staticmethod
    def generate_script(configuration, plugin_code = []):
        '''
        Generate the frida scripts according to the configuration
        :param configuration:
        :return:
        '''
        logging.debug("Frida:generate_script()")

        script = "Java.perform(function(){\n"

        if configuration['FRIDA'].getboolean('anti_emulator'):

            script = "const anti_emulator = require('./lib/anti-emulator.js')\n" + script
            anti_emulator = configuration['ANTI_EMULATOR'].items()
            for item_name, selected in anti_emulator:
                if selected == 'yes':
                    script += f"\tanti_emulator.{item_name}()\n"

        if configuration['FRIDA'].getboolean('hooks'):

            script = "const hooks = require('./lib/hooks.js')\n" + script
            anti_emulator = configuration['HOOKS'].items()
            for item_name, selected in anti_emulator:
                if selected == 'yes':
                    script += f"\thooks.{item_name}()\n"

        for name,code in plugin_code:
            script += f"\t//Plugin code : {name}\n \t{code}\n"
        script += "})"

        return script
