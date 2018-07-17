

def read_file_and_convert_to_list(file_path, ignore_comment=True):
    """
    This method read in file and convert it to list, separated by line-breaker
    :param file_path: path to the file
    :param ignore_comment: if True, will ignore the line start with '#'; if False, read all.
    :return: list of strings
    """
    try:
        trans = []
        with open(file_path) as f:
            lines = f.read().splitlines()

            for line in lines:
                if not line or line.startswith('#'):
                    pass
                else:
                    trans.append(line)
        return trans
    except:
        return []

