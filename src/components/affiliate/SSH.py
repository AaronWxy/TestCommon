import paramiko
import time
from paramiko import SSHClient
from paramiko import SSHException
from paramiko import AuthenticationException
from paramiko import BadHostKeyException
from src.resource.constants import *


class SSH(object):

    def __init__(self, Krakken):
        
        self.krakken = Krakken
        self.logger = Krakken.logger
        self.connection = SSHClient()
        self.connection.load_system_host_keys()

    def connect(self, host, user=DEFAULT_USERNAME, password=DEFAULT_PASSWORD):
        if host in self.krakken.ip_map:
            host = self.krakken.ip_map.get(host)
        self.logger.info("Open SSH connection to " + host)
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.logger.info("PASSWORDLESS: " + str(self.krakken.passwordless))
        if self.krakken.pkey:
            self.logger.info("Using Privatekey: " + self.krakken.pkey)
        try:
            self.disconnect()
            self.logger.hibernate(1)
            self.logger.info("Connecting ... ")
            if not self.krakken.pkey:
                self.connection.connect(
                    host, username=user, password=password, look_for_keys=self.krakken.passwordless, banner_timeout=10)
            else:
                self.connection.connect(host, username='ubuntu', password=password, look_for_keys=self.krakken.passwordless, 
                banner_timeout=10, pkey=self.krakken.pkey)
        except (AuthenticationException, BadHostKeyException) as e:
            self.logger.error(e)
            pytest.fail("Connection failed to host: " + host)
        except SSHException:
            self.logger.warn("Connection failed, will retry after 30s!")
            self.logger.hibernate(30, True)
            self.logger.info("Connecting ... Attempt #2")
            try:
                if not self.krakken.pkey:
                    self.connection.connect(
                        host, username=user, password=password, look_for_keys=self.krakken.passwordless, banner_timeout=10)
                else:
                    self.connection.connect(host, username='ubuntu', password=password, look_for_keys=self.krakken.passwordless, 
                    banner_timeout=10, pkey=self.krakken.pkey)
            except (AuthenticationException, BadHostKeyException, SSHException) as e:
                self.logger.error(e)
                pytest.fail("Connection failed to host: " + host)
            else:
                self.logger.info("Connected!")
        else:
            self.logger.info("Connected!")

    def blocking_call(self, command, verbose=False, console=True, timeout=None):
        start_time = time.time() 
        self.logger.info("Executing Command: ")
        self.logger.info("Krakken > " + command)
        if timeout:
            self.logger.info("Timeout = " + str(timeout))
        self.fix_channel()
        if self.krakken.pkey:
            command = 'sudo su {} -c """'.format(DEFAULT_USER) + command.replace('"', '\\"') + '"""'
        if console:
            self.logger.info(" ")
            self.logger.info("=" * 80)
            self.logger.info("[STD_OUT]")
        stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)

        stdout_list, stderr_list = [], []
        while not stdout.channel.exit_status_ready():
            for line in iter(stdout.readline, ""):
                if console:
                    try:
                        print line,
                    except UnicodeEncodeError:
                        print line.encode('utf-8'),
                if line.strip():
                    stdout_list.append(line.strip())
            for line in iter(stderr.readline, ""):
                if console:
                    try:
                        print line,
                    except UnicodeEncodeError:
                        print line.encode('utf-8'),
                if line.strip():
                    stderr_list.append(line.strip())
        rc = stdout.channel.recv_exit_status()
        end_time = time.time()
        mins, seconds = divmod(end_time - start_time, 60)
        millseconds = (seconds - int(seconds)) * 1000
        if not mins and not seconds:
            elapse = "{} ms".format(int(millseconds))
        elif not mins:
            elapse = "{} s {} ms".format(int(seconds), int(millseconds))
        else:
            elapse = "{} min {} s {} ms".format(int(mins), int(seconds), int(millseconds))
        self.logger.info("Command Complete in {}!".format(elapse))
        if stdout_list:
            with open(self.krakken.logger.current_info, 'w+') as f:
                f.write("\n".join(stdout_list))
        if stderr_list:
            with open(self.krakken.logger.current_error, 'w+') as f:
                f.write("\n".join(stderr_list))
        if console:
            self.logger.info(" ")
            self.logger.info("=" * 80)
        if not verbose:
            return rc 
        else:
            return rc, stdout_list, stderr_list

    def non_blocking_call(self, command):
        
        self.fix_channel()
        self.logger.info("Executing non-blocking command: ")
        self.logger.info("Krakken > " + command)
        if self.krakken.pkey:
            command = 'sudo su {} -c """'.format(DEFAULT_USER) + command.replace('"', '\\"') + '"""'
        stdin, stdout, stderr = self.connection.exec_command(command)
        self.logger.info("Command sent!")
        stdin.close()

    def disconnect(self):
        self.logger.info("Closing ssh connection!")
        try:
            self.connection.close()
        except AttributeError:
            pass

    def fix_channel(self):
        if not self.connection or not self.connection.get_transport() or not self.connection.get_transport().is_active():
            self.logger.warn("SSH Connection is not opened yet, connecting to default master node .. ")
            self.connect(self.krakken.master)
