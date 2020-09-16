import traceback
from datetime import datetime
import time

FIELDS = [
    'time',
    'date',
    'file',
    'error_doc',
    'full_traceback',
    'string_number',
    'exeption_name'
]


class Logger:

    def __init__(self, log_file='log_file.txt', fields=None):
        self.log_file = log_file
        self.local_time = time.localtime()
        self.fields = fields

    def save_error(self, error):
        with open(self.log_file, 'a') as log_file:
            log_file.write(self._make_log_string(error))

    def time(self):
        return self._get_time()

    def date(self):
        return self._get_date()

    def file(self):
        return self._get_tracback_file()

    def error_doc(self):
        return self.error.__doc__

    def _make_log_string(self, error):
        self.error = error
        values = self._get_values()
        string = ''
        i = 0
        for arg in values:
            if (i % 3) == 0 and i:
                string += '\n' + ' ' * (len(values[0]) + 3) if (len(values[0]) <= 10) else 10
            string += f'[{arg}] '
            i += 1

        return string + '\n'

    def _get_values(self):
        if self.fields is None:
            return [self._get_time(), self._get_date(), self._get_tracback_file(), self.error_doc()]
        else:
            value_arr = []
            for value in self.fields:
                # value_arr.append(eval(f'self.{value}'))
                ret = eval(f'self.{value}')()
                value_arr.append(ret)
            return value_arr

    def _get_time(self):
        return time.strftime("%H:%M:%S", self.local_time)

    def _get_date(self):
        return datetime.now().date()

    def _get_tracback_file(self):
        return traceback.StackSummary.extract(traceback.walk_stack(None))[1].filename
