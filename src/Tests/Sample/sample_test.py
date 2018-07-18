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
        pytest.fail("test failure")

    def test_4(self):
        pytest.skip("skip test")
