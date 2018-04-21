__author__ = 'geb'

import pkgutil

data = pkgutil.get_data('efweb', 'data/error_status.dat')

responses = {line.split(" ")[0]: " ".join(line.split(" ")[1:]) for line in data.decode("utf-8").split('\r\n')}
