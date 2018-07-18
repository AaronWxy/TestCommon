from ConfigParser import ConfigParser 


def write_options_dict_to_config(config_file, section, data):
    parser = ConfigParser()
    parser.optionxform = str
    parser.add_section(section)
    for key in data.keys():
        parser.set(section, key, data[key])
    with open(config_file, 'w') as f:
        parser.write(f)
