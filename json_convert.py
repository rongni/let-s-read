import json


def write_json(data, json_file):
    """ write to json helper function

    Args:
        data (string): data to write
        json_file (json): json file write to
    """
    json.dump(data, open(json_file, 'w'))
    # json.dump(data, open(json_file, 'w'))


def write_data(json_file):
    """write data"""
    with open(json_file) as file:
        file_data = json.load(file)
    return file_data
