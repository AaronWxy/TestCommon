import logging
import os
import shutil
import time


class Logger(object):

    LOG_FORMAT = '%(asctime)s [%(levelname)-5s] %(message)s' 
    LOG_FILE_INFO = 'test.inf.log'
    LOG_FILE_ERROR = 'test.err.log'
    BASE_LOG_LEVEL = logging.DEBUG
    test_step = 0
    krakken_logger = None

    def __init__(self, base_folder="Output/"):
        """[Basic Logger Object]
        
        Keyword Arguments:
            base_folder {str} -- [the logger output location] (default: {"Output/"})
        """

        self.base_folder = base_folder

        # init the basic logger object
        if self.krakken_logger:
            krakken_logger = self.krakken_logger
        else:
            krakken_logger = logging.getLogger('Krakken')
            krakken_logger.setLevel(logging.DEBUG)

        # create log folder if not exists
        if not os.path.isdir(base_folder):
            os.mkdir(base_folder)
        if not os.path.isdir(base_folder+str(self.test_step)+'/'):
            os.mkdir(base_folder+str(self.test_step)+'/')
        if not os.path.isfile(base_folder+str(self.test_step)+'/'+self.LOG_FILE_INFO):
            with open(base_folder+str(self.test_step)+'/'+self.LOG_FILE_INFO, 'a'):
                self.current_info = base_folder+str(self.test_step)+'/'+self.LOG_FILE_INFO
        if not os.path.isfile(base_folder+str(self.test_step)+'/'+self.LOG_FILE_ERROR):
            with open(base_folder+str(self.test_step)+'/'+self.LOG_FILE_ERROR, 'a'):
                self.current_error = base_folder+str(self.test_step)+'/'+self.LOG_FILE_ERROR 

        for handler in krakken_logger.handlers[:]:
            krakken_logger.removeHandler(handler)

        # set streaming logging to console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)-5s] %(message)s')
        console.setFormatter(formatter)
        krakken_logger.addHandler(console)

        # set the default logging to file test.inf.log
        file_handler_info = logging.FileHandler(
            base_folder+str(self.test_step)+'/'+self.LOG_FILE_INFO, mode='w', encoding='utf-8')
        file_handler_info.setFormatter(logging.Formatter(self.LOG_FORMAT))
        file_handler_info.setLevel(logging.DEBUG)
        krakken_logger.addHandler(file_handler_info)

        # set file logging to test.err.log for level ERROR and above
        file_handler_err = logging.FileHandler(
            base_folder+str(self.test_step)+'/'+self.LOG_FILE_ERROR, mode='w', encoding='utf-8')
        file_handler_err.setFormatter(logging.Formatter(self.LOG_FORMAT))
        file_handler_err.setLevel(logging.ERROR)
        krakken_logger.addHandler(file_handler_err)

        self.info = krakken_logger.info  
        self.warn = krakken_logger.warn 
        self.error = krakken_logger.error
        self.debug = krakken_logger.debug

        self.krakken_logger = krakken_logger


    def step_registry(self):
        """[Move the point to next and recreate the logger object]
        """

        self.test_step += 1
        # print "registering >> " + str(self.test_step)
        self.__init__()

    
    def hibernate(self, sleep_time=5, callback=False, purpose=""):
        if not purpose:
            self.info("Hibernating for " + str(sleep_time) + " sec")
        else:
            self.info("Hibernating for " + str(sleep_time) + "to: " + purpose)
        time.sleep(sleep_time)
        if callback:
            self.info("Wake Up!")
