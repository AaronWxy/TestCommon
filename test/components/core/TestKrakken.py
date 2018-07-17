from src.components.core.Krakken import Krakken
from src.components.core.Logger import Logger


def main():
    # test 1
    krakken = Krakken("host1", "4.1.0", "4.1.2")
    assert len(krakken.hosts) == 1
    assert krakken.hosts[0] == "host1"
    assert krakken.ip_map.get(krakken.hosts[0]) is None
    assert krakken.version == "4.1.0"
    assert krakken.content_version == "4.1.2"
    assert krakken.variant == ""
    assert krakken.suite == ""
    assert krakken.config == ""
    assert isinstance(krakken, Krakken)
    assert isinstance(krakken.logger, Logger)
    # test 2
    krakken = Krakken("host1,host2,host3", "4.1.0", ips="1.1.1.1,1.1.1.2,1.1.1.3", variant="AWS", suite="Beta", test_config="config/config2.ini")
    assert len(krakken.hosts) == 3
    assert krakken.hosts[0] == "host1"
    assert krakken.ip_map.get(krakken.hosts[0]) == "1.1.1.1"
    assert krakken.ip_map.get(krakken.hosts[2]) == "1.1.1.3"
    assert krakken.version == "4.1.0"
    assert krakken.content_version == "4.1.0"
    assert krakken.variant == "AWS"
    assert krakken.suite == "Beta"
    assert krakken.config == "config/config2.ini"
    assert isinstance(krakken, Krakken)
    assert isinstance(krakken.logger, Logger)

if __name__ == "__main__":
    main()