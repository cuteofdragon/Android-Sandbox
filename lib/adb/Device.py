import subprocess
import logging


class Device:

    def __init__(self, path_config, configuration, type):
        self.adb_path = path_config.get('adb_path')
        self.emulator_path = path_config.get('emulator_path')

        self.type = type
        self.configuration = configuration
        self.device_id = None

    def list_devices(self):
        '''
        List current device recognized by adb and sort them by type (emulator|physical)
        :return:
        '''
        logging.debug("Device:listing_devices()")

        # Get list of launched devices
        pid = subprocess.Popen([self.adb_path, 'devices'], stdout=subprocess.PIPE)
        pid.wait()

        raw_result = pid.communicate()[0].strip()
        devices = raw_result.split(b'\n')[1:]

        result = {
            'emulator': [],
            'physical': []
        }

        for device in devices:
            name, state = device.split(b'\t')
            if name.startswith(b'emulator'):
                result['emulator'].append(name.decode('utf8'))
            else:
                result['physical'].append(name.decode('utf8'))

        return result

    def check_is_up(self):
        '''
        Return if the phone has booted up.
        It returns "true" when you the lockscreen is unlocked
        :return:
        '''
        pid = subprocess.Popen([self.adb_path, '-s', self.device_id, 'shell', 'getprop', 'dev.bootcomplete'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        pid.wait()
        return b'1' in pid.communicate()[0]

    def kill_emulators(self):
        '''
        Kill all current emulators
        :return:
        '''
        logging.debug("Device:kill_emulators()")
        devices = self.list_devices()

        # Killing all running devices
        for device in devices['emulator']:
            pid = subprocess.Popen([self.adb_path, '-s', device, 'emu', 'kill'], stdout=subprocess.PIPE)
            pid.wait()

    def check_application_is_running(self, package_name):
        '''
        Verify that an application is launched ( Android > 7 )
        :param package_name:
        :return:
        '''
        logging.debug('Device:check_application_is_running()')

        pid = subprocess.Popen([self.adb_path,'-s', self.device_id, 'shell', 'pidof', package_name], stdout= subprocess.PIPE)
        pid.wait()
        return b'' == pid.communicate()[0]

    def install_application(self, path):
        '''
        Install the given application on the device
        :param path:
        :return:
        '''
        logging.debug("Device:install_application()")
        pid = subprocess.Popen([self.adb_path,'-s',self.device_id, 'install', path],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        pid.wait()
        stdout, stderr = pid.communicate()
        if stderr != b'':
            logging.error(f"Error while installing application {path} : {stderr}")
        else:
            logging.info(f'Installed')

    def install_frida(self):
        '''
        Install Frida using `frida-push`
        :return:
        '''
        logging.debug("Device:install_frida()")
        if(self.type == 'Physical'):
            logging.info("You must launch firda manually")
        else:
            pid = subprocess.Popen(['frida-push', '-d', self.device_id],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            pid.wait()
            stdout, stderr = pid.communicate()
            if stderr != b'':
                logging.error(f"Error while installing frida : {stderr}")
            else:
                logging.info(f'Frida Installed')

    def install_certificate(self, certificate_path):
        logging.debug("Device:install_certificate()")
        if(self.type == "Physical"):
            logging.info("You need to install the certificate manually ( go to http://mitm.it ) ")



    def uninstall_application(self,package_name):
        '''
        Uninstal the application given by the package name
        :param package_name:
        :return:
        '''
        logging.debug("Device:uninstall_application()")
        pid = subprocess.Popen([self.adb_path, '-s', self.device_id, 'uninstall', package_name],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        pid.wait()
        stdout, stderr = pid.communicate()
        if stderr != b'':
            logging.error(f"Error while installing application {package_name} : {stderr}")
        else:
            logging.info(f'Uninstalled')

    def launch_application(self, package_name):
        '''
        Launch an application using adb monkey
        :param package_name:
        :return:
        '''
        logging.debug("Device:launch_application()")
        pid = subprocess.Popen([self.adb_path, '-s', self.device_id, 'shell', 'monkey', '-p', package_name, '-v', '1'], stdout=subprocess.PIPE)
        pid.wait()
        stdout, stderr = pid.communicate()
        if stderr:
            logging.error(f"Error while launching application {package_name} : {stderr}")
        else:
            logging.debug(f'Launched !')

    def start(self):
        logging.error("Device:start() should not be called on the superclass")
