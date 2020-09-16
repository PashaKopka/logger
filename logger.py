from abc import ABC, abstractmethod
from datetime import datetime

import time
import traceback

FIELDS = [
    'time',
    'date',
    'file',
    'error_doc',
    'full_traceback',
    'line',
    'exception_name'
]


class FileWorker:

    def __init__(self, file_name):
        self.file_name = file_name

    def save_value(self, value: str):
        with open(self.file_name, 'a') as log_file:
            log_file.write(value)


class LogMaker:

    @staticmethod
    def make_log_string(names, values, fields):
        names = [(value if value in names else '') for value in fields]
        string = ''
        i = 0
        for name, arg in zip(names, values):
            if (i % 3) == 0 and i:
                string += '\n' + ' ' * (len(values[0]) + 3) if (len(values[0]) <= 10) else 10

            if name:
                string += f'[{name.title()}: {arg}] '
            else:
                string += f'[{arg}] '
            i += 1

        return string + '\n'


class Logger:

    def __init__(self, log_file='log_file.txt', fields=None, named_fields=None):
        self.log_file = log_file
        self.local_time = time.localtime()
        self.fields = fields if fields else ['time', 'date', 'file', 'error_doc']
        self.named_fields = named_fields if named_fields else []

        self.file_worker = FileWorker(self.log_file)
        self.log_maker = LogMaker()

        self.error = None

    def save_error(self, error):
        self.error = error
        value = self.log_maker.make_log_string(self.named_fields, self._get_values(), self.fields)
        self.file_worker.save_value(value)

    def _get_values(self):
        value_arr = []
        for value in self.fields:
            ret = eval(f'self.{value}')
            value_arr.append(ret)
        return value_arr

    @property
    def time(self):
        return self._get_time()

    @property
    def date(self):
        return self._get_date()

    @property
    def file(self):
        return self._get_tracback_file()

    @property
    def line(self):
        return self._get_tracback_line()

    @property
    def error_doc(self):
        return self.error.__doc__

    def _get_time(self):
        return time.strftime("%H:%M:%S", self.local_time)

    @staticmethod
    def _get_date():
        return datetime.now().date()

    @staticmethod
    def _get_tracback_file():
        return traceback.StackSummary.extract(traceback.walk_stack(None))[-1].filename

    @staticmethod
    def _get_tracback_line():
        return traceback.StackSummary.extract(traceback.walk_stack(None))[-1].lineno
