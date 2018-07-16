import logging


class Logger(object):

    LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s' 
    LOG_FILE_INFO = 'test.inf.log'
    LOG_FILE_ERROR = 'test.err.log'
    BASE_LOG_LEVEL = logging.DEBUG
    test_step = 0

    def __init__(self, base_folder="Main/Output/"):
        """[Basic Logger Object]
        
        Keyword Arguments:
            base_folder {str} -- [the logger output location] (default: {"Output/"})
        """

        # init the basic logger object
        krakken_logger = logging.getLogger('Krakken')

        # set streaming logging to console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        krakken_logger.addHandler(console)

        # set the default logging to file test.inf.log
        file_handler_info = logging.FileHandler(
            base_folder+str(self.test_step)+'/'+self.LOG_FILE_INFO, mode='w')
        file_handler_info.setFormatter(self.LOG_FORMAT)
        file_handler_info.setLevel(logging.DEBUG)
        logging.getLogger('').addHandler(file_handler_info)

        # set file logging to test.err.log for level ERROR and above
        file_handler_err = logging.FileHandler(
            base_folder+str(self.test_step)+'/'+self.LOG_FILE_ERROR, mode='w')
        file_handler_err.setFormatter(self.LOG_FORMAT)
        file_handler_err.setLevel(logging.ERROR)
        logging.getLogger('').addHandler(file_handler_err)

        self.info = krakken_logger.info  
        self.warn = krakken_logger.warn 
        self.error = krakken_logger.error
        self.debug = krakken_logger.debug

    def test_step_registry(self):
        """[Move the point to next and recreate the logger object]
        """

        self.test_step += 1
        self.__init__()
