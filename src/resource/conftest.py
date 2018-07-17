import pytest
import time 
import pprint
import socket
from src.components.core.Krakken import Krakken
from _pytest.runner import runtestprotocol


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

# this run before all
@pytest.fixture(scope="function", autouse=False)
def init_suite(HOSTS, VERSION, CONTENTVERSION, IPS, VARIANT, SUITE, CONFIG, request):
    k = Krakken(HOSTS, VERSION, CONTENTVERSION, IPS, VARIANT, SUITE, CONFIG)
    global krakken
    krakken = k
    print type(krakken)
    return k


# this run before each
@pytest.fixture(autouse=True)
def step_init(request):
    # prepare something ahead of all tests
    # print "Runs once before each test"

    def regi():
        print "GOGOGO"
        global krakken
        krakken.logger.step_registry()

    request.addfinalizer(regi)
    

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
def pytest_runtest_protocol(item, nextitem, starttime=0):
    reports = runtestprotocol(item, nextitem=nextitem)
    cases, status = [], []
    for report in reports:
        # h, r = divmod(report.duration, 3600)
        # m, s = divmod(r, 60)
        # time_elapsed = "{:0>2}h:{:0>2}m:{:05.2f}s".format(int(h), int(m), s)
        try:
            t = report.duration
            time_elapsed = ("{:0>2}h:".format(int(t//3600)) if int(t//3600) > 0 else "") 
            + ("{:0>2}m:".format(int(t - 3600 * (t//3600))//60) if (t - 3600 * (t//3600))//60 > 0 
            or t//3600>0 else "") + "{:05.2f}s".format(t%60)
        except:
            time_elapsed = "-"
        if report.when == 'call':
            global cnt, results_collection, case_start_time
            c_end_time = time.time()
            if report.outcome == 'passed':
                current = Result(cnt, item.name, 0, case_start_time, c_end_time)
            elif report.outcome == 'failed':
                current = Result(cnt, item.name, 2, case_start_time, c_end_time)
            else:
                current = Result(cnt, item.name, 1, case_start_time, c_end_time)
            results_collection.append(current)
            cnt += 1 
            case_start_time = c_end_time


def pytest_sessionfinish(session, exitstatus):
    for res in results_collection:
        print "COUNTER: " + str(res.counter)
        print "RC: " + str(res.rc)
    # report_wrapping(start_time)

