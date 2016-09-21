import pprint as python_pprint

class LyricNotFound(Exception):
    pass

def pprint(data):
    pp = python_pprint.PrettyPrinter(indent=4)
    pp.pprint(data)
    return pp.pformat(data)