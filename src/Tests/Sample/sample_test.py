import pytest
import pprint
from src.components.core.Krakken import Krakken

class TestSample:

    krakken = None
    logger = None
    
    def test_configuration(self, init_suite):
        self.__class__.krakken = init_suite
        self.logger = self.__class__.krakken.logger
        self.krakken.logger.info("CASE0")

    def test_1(self):
        self.__class__.krakken.logger.info("CASE1")

    def test_2(self):
        self.__class__.krakken.logger.info("CASE2")

    def test_3(self):
        pytest.fail("test failure")
