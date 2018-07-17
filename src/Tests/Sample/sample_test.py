import pytest
import pprint
from src.components.core.Krakken import Krakken

class TestSample(object):

    krakken = None
    logger = None
    
    def test_configuration(self, get_krakken):
        self.__class__.krakken = get_krakken
        self.__class__.logger = self.__class__.krakken.logger

    def test_1(self):
        self.__class__.krakken.logger.step_registry()
        self.__class__.logger.info("CASE1")

    def test_2(self):
        self.__class__.krakken.logger.step_registry()
        self.__class__.logger.info("CASE2")
