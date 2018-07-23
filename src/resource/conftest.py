import pytest
import time 
import pprint
import socket
from src.components.core.Krakken import Krakken
from _pytest.runner import runtestprotocol
from pytest import Function
from functools import wraps


cnt = 0
start_time = 0
case_start_time = 0
test_name_dic = {}
krakken = None
results_collection = []
host = socket.gethostname()

def pytest_addoption(parser):
    parser.addoption("--HOSTS", action="store", help="provide the hostnames, separated by comma")
    parser.addoption("--VERSION", action="store", help="provide the platform version")
    parser.addoption("--CONTENTVERSION", action="store", default="", help="optional: provide the content version")
    parser.addoption("--IPS", action="store", default="", help="optional: provide the content version")
    parser.addoption("--VARIANT", action="store", default="", help="optional: provide the variant of system")
    parser.addoption("--SUITE", action="store", default="", help="optional: provide the variant of test suite")
    parser.addoption("--CONFIG", action="store", default="", help="optional: provide the extra config file for testing")
    parser.addoption("--PASSWORDLESS", action="store", default=False, help="optional: if using passwordless connection")
    parser.addoption("--PRIVATEKEY", action="store", default="", help="optional: provide privatekey location")


@pytest.fixture(scope="session")
def HOSTS(request):
    return request.config.getoption("--HOSTS")

@pytest.fixture(scope="session")
def VERSION(request):
    return request.config.getoption("--VERSION")

@pytest.fixture(scope="session")
def CONTENTVERSION(request):
    return request.config.getoption("--CONTENTVERSION")

@pytest.fixture(scope="session")
def IPS(request):
    return request.config.getoption("--IPS")

@pytest.fixture(scope="session")
def VARIANT(request):
    return request.config.getoption("--VARIANT")

@pytest.fixture(scope="session")
def SUITE(request):
    return request.config.getoption("--SUITE")

@pytest.fixture(scope="session")
def CONFIG(request):
    return request.config.getoption("--CONFIG")

@pytest.fixture(scope="session")
def PASSWORDLESS(request):
    return request.config.getoption("--PASSWORDLESS")

@pytest.fixture(scope="session")
def PRIVATEKEY(request):
    return request.config.getoption("--PRIVATEKEY")

# this run before all
@pytest.fixture(scope="function", autouse=False)
def init_suite(HOSTS, VERSION, CONTENTVERSION, IPS, VARIANT, SUITE, CONFIG, PASSWORDLESS, PRIVATEKEY, request):
    k = Krakken(HOSTS, VERSION, CONTENTVERSION, IPS, VARIANT, SUITE, CONFIG, PASSWORDLESS, PRIVATEKEY)
    global krakken
    krakken = k
    request.config._metadata["TEST SUITE"] = "Mode Test"
    if krakken.master in krakken.ip_map:
        request.config._metadata["HOST"] = krakken.ip_map.get(krakken.master)
    else:
        request.config._metadata["HOST"] = krakken.master
    request.config._metadata["VERSION"] = krakken.version
    request.config._metadata["CONTENT"] = krakken.content_version
    request.config._metadata["START TIME"] = str(time.ctime())
    mandentory_delete = [
            'BUILD_ID',
            'BUILD_NUMBER',
            'GIT_COMMIT',
            'Python',
            'NODE_NAME',
            'BUILD_TAG',
            'Platform',
            'WORKSPACE',
            'Plugins',
            'Packages'
    ]
    for key in list(request.config._metadata):
        if key in mandentory_delete:
            del request.config._metadata[key]
    krakken.reporter.log_meta_data(request)
    return k


# this run before each
@pytest.fixture(autouse=True)
def step_init(request):
    # prepare something ahead of all tests
    # print "Runs once before each test"

    global krakken
    if krakken:
        krakken.logger.step_registry()
    else:
        init_suite
    

class Result:

    def __init__(self, count=0, func="", rc=0, c_start_time=0, c_end_time=0):
        self.counter = count
        self.func = func
        self.rc = rc


def pytest_sessionstart(session):
    global start_time
    global case_start_time
    start_time = time.time()
    case_start_time = start_time

# def record_pytest_result(item, nextitem, test_name_dic, starttime=0):
def pytest_runtest_protocol(item, nextitem):
    reports = runtestprotocol(item, nextitem=nextitem)
    # print "ACD" + str(len(reports))
    for report in reports:
        # h, r = divmod(report.duration, 3600)
        # m, s = divmod(r, 60)
        # time_elapsed = "{:0>2}h:{:0>2}m:{:05.2f}s".format(int(h), int(m), s)
        # print "A: " + str(report.when)
        """if report.when == 'call':
            print '\n%s --- %s' % (item.name, report.outcome)"""
        # print (item.name, report.outcome, report.when)
        return True
        

def pytest_sessionfinish(session, exitstatus):
    for res in results_collection:
        print "COUNTER: " + str(res.counter)
        print "RC: " + str(res.rc)

    krakken.reporter.record_results()
    krakken.reporter.create_report()
    krakken.sftp.close_sftp()
    krakken.ssh.disconnect()
    # report_wrapping(start_time)
    


@pytest.fixture(autouse=True)
def log_case_start_time(record_property):
    record_property("case_start_time", time.time())

