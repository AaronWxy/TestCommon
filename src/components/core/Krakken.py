import pprint 
from src.components.core.Logger import Logger


class Krakken(object):

    def __init__(self, hosts, ips, test_config, version, content_version=None, variant=None, suite=None):
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
        self.ip_map = dict(zip(self.hosts, ips.split(",")))
        self.version = version
        self.content_version = (content_version if content_version else version)
        self.variant = variant
        self.suite = suite 
        self.logger = Logger()
        self.config = test_config
