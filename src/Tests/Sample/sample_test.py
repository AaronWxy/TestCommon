import pytest
import pprint
from src.components.core.Krakken import Krakken

class TestSample:

    krakken = None
    logger = None
    
    def test_configuration(self, init_suite, request):
        self.__class__.krakken = init_suite
        self.logger = self.__class__.krakken.logger
        # TODO: record meta data
        self.__class__.krakken.reporter.log_meta_data(request)
        self.krakken.logger.info("CASE0")
        self.__class__.krakken.logger.hibernate(1)

    def test_1(self):
        self.__class__.krakken.logger.info("CASE1")
        self.__class__.krakken.logger.hibernate(1)

    def test_2(self):
        self.__class__.krakken.logger.info("CASE2")
        self.__class__.krakken.logger.hibernate(1)

    def test_3(self):
        self.__class__.krakken.ssh.connect(self.__class__.krakken.master)
        self.__class__.krakken.ssh.blocking_call("ls -a")

    def test_4(self):
        self.__class__.krakken.ssh.connect(self.__class__.krakken.master)
        self.__class__.krakken.sftp.open_sftp()
        self.__class__.krakken.sftp.grab_from_remote_path('/var/log/caspida/caspida.out', 'Output/')

    