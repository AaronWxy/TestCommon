from ConfigParser import ConfigParser 

# config
def read_option_from_config(config_file, section, opt):
    """
    :param file: config file path
    :param section: sections to read
    :param opt: options to read
    :return: value
    """
    parser = ConfigParser()
    parser.optionxform = str
    try:
        parser.read(config_file)
        return parser.get(section,opt)
    except:
        return None


def read_options_as_dict_from_config(config_file, section):
    """
    This method read one properties file for one section, and return all key-value pair in dictionary
    :param file: path to the properties file
    :param section: section to process
    :return: key-value pair dictionary
    """
    parser = ConfigParser()
    parser.optionxform = str
    try:
        ret = {}
        parser.read(config_file)
        opts = parser.options(section)
        for opt in opts:
            ret[opt] = parser.get(section, opt)
        return ret
    except:
        return {}