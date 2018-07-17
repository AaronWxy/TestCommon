import pprint 
from src.components.core.Logger import Logger


class Krakken(object):

    def __init__(self, hosts, version, content_version="", ips="", variant="", suite="", test_config=""):
        """[Base Test Object]
        
        Arguments:
            hosts {[str]} -- [input string of distributed nodes' hostnames, separated by comma]
            ips {[str]} -- [input string of distributed nodes' ips, separated by comma]
            version {[str]} -- [app platform version]
            content_version {[str]} -- [app content version]
            variant {[str]} -- [input the variant of test object, this parameter can be used to track such as different platform]
            suite {[str]} -- [input the suite to execute, if any]
        """
        self.hosts = hosts.split(",")
        self.ip_map = dict(zip(self.hosts, ips.split(","))) if ips else {}
        self.master = self.hosts[0]
        self.version = version
        self.content_version = (content_version if content_version else version)
        self.variant = variant
        self.suite = suite 
        self.logger = Logger()
        self.config = test_config
        # DEBUG:
        self.logger.debug("\n")
        self.logger.debug("HOSTS: " + pprint.pformat(self.hosts))
        self.logger.debug("MASTER: " + pprint.pformat(self.master))
        self.logger.debug("VERSION: " + pprint.pformat(self.version))
        self.logger.debug("CONTENTVERSION: " + pprint.pformat(self.content_version))
        self.logger.debug("IP_MAPPING: " + pprint.pformat(self.ip_map))
        self.logger.debug("VARIANT: " + pprint.pformat(self.variant))
        self.logger.debug("SUITE: " + pprint.pformat(self.suite))
        self.logger.debug("TEST_CONFIG: " + pprint.pformat(self.config))
