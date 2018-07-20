import pytest
import subprocess
import shutil

class TestFramework(object):

    debug = True

    def test_logger(self):
        command = "python test/components/core/TestLogger.py"
        command = command.split()
        try:
            subprocess.check_output(command)
        except subprocess.CalledProcessError, e:
            pytest.fail("Failed")

    def test_krakken_1(self):
        command = "python test/components/core/TestKrakken.py"
        command = command.split()
        try:
            subprocess.check_output(command)
        except subprocess.CalledProcessError, e:
            pytest.fail("Failed")

    def test_wrapper(self):
        if not self.__class__.debug:
            print "deleting the logs"
            shutil.rmtree("Output")
        else:
            print "DEBUG is set to True, will not delete Output"
