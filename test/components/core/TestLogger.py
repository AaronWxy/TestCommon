import os
from src.components.core.Logger import Logger

def main():
    test_logger = Logger()
    test_logger.info("TEST 1: only see me on console and in inf file")
    test_logger.error("TEST 2: see me every where")
    test_logger.debug("TEST 3: only see me in inf file")
    test_logger.warn("TEST 4: only see me in inf file and console")
    test_logger.step_registry()
    test_logger.info("TEST 5: only see me on console and in inf file, in new folder")
    test_logger.error("TEST 6: see me every where, in new folder")
    test_logger.debug("TEST 7: only see me in inf file, in new folder")
    test_logger.warn("TEST 8: only see me in inf file and console, in new folder")

    assert os.path.isdir("Output/0/")
    assert os.path.isdir("Output/1/")
    assert os.path.isfile("Output/0/test.inf.log")
    assert os.path.isfile("Output/0/test.err.log")
    assert os.path.isfile("Output/1/test.inf.log")
    assert os.path.isfile("Output/1/test.err.log")
    assert 'only see me on console and in inf file' in open("Output/0/test.inf.log").read()

if __name__ == "__main__":
    main()