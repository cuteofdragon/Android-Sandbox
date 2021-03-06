from .Device import Device

import subprocess
import logging
import time


class Emulator(Device):
    """
    Emulator controller, extends Device
    """

    def __init__(self, path_config, configuration, ):
        Device.__init__(self, path_config, configuration, 'Emulator')

    def install_certificate(self, certificate_path):
        '''
        Install the user certificate to the phone ( see scripts/install_cert.sh )
        Needed for mitmproxy to intercept SSL.
        :param certificate_path:
        :return:
        '''
        pid = subprocess.Popen(['bash', 'scripts/install_cert.sh', certificate_path, self.device_id],stdout=subprocess.DEVNULL)
        pid.wait()

        while not self.check_is_up():
            time.sleep(0.5)

    def start(self):
        '''
        Start the emulator according to the given configuration
        :return:
        '''
        logging.debug("Emulator:start()")

        self.kill_emulators()

        emulator_config = [self.emulator_path]

        # Setting vm_name
        vm_name = self.configuration['EMULATOR'].get('vm_name')
        emulator_config.append(f"@{vm_name}")

        # Setting snapshot
        if self.configuration['EMULATOR'].getboolean('use_snapshot'):
            snapshot_name = self.configuration['EMULATOR'].get('snapshot_name')
            emulator_config.append('-snapshot')
            emulator_config.append(snapshot_name)

        # Setting window
        if not self.configuration['EMULATOR'].getboolean('show_window'):
            emulator_config.append('-no-window')

        # Setting wipe emulator
        if self.configuration['EMULATOR'].getboolean('wipe_data'):
            emulator_config.append('-wipe-data')

        emulator_config.append('-no-audio')

        if self.configuration['ANALYSIS'].getboolean('use_proxy'):
            emulator_config.append('-http-proxy')
            port = self.configuration['PROXY'].getint('port')
            emulator_config.append(f"http://0.0.0.0:{port}")
            emulator_config.append('-writable-system')

        logging.debug(f"Launching emulator : {emulator_config}")

        subprocess.Popen(emulator_config, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        devices = self.list_devices()['emulator']

        logging.debug("Waiting for device_id")
        while len(devices) < 1:
            time.sleep(0.5)
            devices = self.list_devices()['emulator']

        self.device_id = devices[0]
        logging.debug(f"Device id : {self.device_id}")

        logging.debug("Checking if it is up")
        while not self.check_is_up():
            time.sleep(0.5)

        logging.info("Emulator launched")
