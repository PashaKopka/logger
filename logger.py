import traceback
from datetime import datetime
import time


class Logger:

    def __init__(self, log_file='log_file.txt'):
        self.log_file = log_file
        self.time = time.localtime()

    def _make_log_string(self, error):
        file_name = traceback.StackSummary.extract(traceback.walk_stack(None))[1].filename
        values = [self._get_time(), self._get_date(), file_name, error.__doc__]
        string = ''
        i = 0
        for arg in values:
            if (i % 3) == 0 and i:
                string += '\n' + ' ' * (len(values[0]) + 3) if (len(values[0]) <= 10) else 10
            string += f'[{arg}] '
            i += 1

        return string + '\n'

    def save_error(self, error):
        with open(self.log_file, 'a') as log_file:
            log_file.write(self._make_log_string(error))

    def _get_time(self):
        return time.strftime("%H:%M:%S", self.time)

    def _get_date(self):
        return datetime.now().date()
