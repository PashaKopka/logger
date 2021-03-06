from abc import ABC, abstractmethod
from datetime import datetime

import time
import traceback

FIELDS = [
    'time',
    'date',
    'file',
    'error_doc',
    'line',
    'exception_name'
]


class FileWorker:

    def __init__(self, file_name: str):
        self.file_name = file_name

    def save_value(self, value: str):
        with open(self.file_name, 'a') as log_file:
            log_file.write(value)


class LogMaker:

    @staticmethod
    def make_log_string(names: list, values: list, fields: list) -> str:
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


class AbstractLogger(ABC):

    def __init__(self):
        self.error = None

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

    @property
    def exception_name(self):
        return self.error.args[0]

    @abstractmethod
    def _get_time(self):
        pass

    @abstractmethod
    def _get_date(self):
        pass

    @abstractmethod
    def _get_tracback_file(self):
        pass

    @abstractmethod
    def _get_tracback_line(self):
        pass


class Logger:

    def __init__(self, log_file='log_file.txt', fields=None, named_fields=None):
        self._input_validate(log_file, fields, named_fields)

        self.log_file = log_file
        self.local_time = time.localtime()
        self.fields = fields if fields else ['time', 'date', 'file', 'error_doc']
        self.named_fields = named_fields if named_fields else []

        self.file_worker = FileWorker(self.log_file)
        self.log_maker = LogMaker()

        self.error = None

    def save_error(self, error: Exception):
        if not isinstance(error, Exception):
            raise TypeError(f'error must be Exception type, not {type(error).__name__}')
        self.error = error
        value = self.log_maker.make_log_string(self.named_fields, self._get_values(), self.fields)
        self.file_worker.save_value(value)

    def _get_values(self) -> list:
        value_arr = []
        for value in self.fields:
            ret = eval(f'self.{value}')
            value_arr.append(str(ret))
        return value_arr

    def _get_time(self):
        return time.strftime("%H:%M:%S", self.local_time)

    @staticmethod
    def _input_validate(log_file: str, fields: list, named_fields: list):
        if not isinstance(log_file, str):
            raise TypeError(f'log_file must be str, not {type(log_file).__name__}')
        if not isinstance(fields, list) and fields is not None:
            raise TypeError(f'fields must be list with str, not {type(fields).__name__}')
        if fields is not None:
            for field in fields:
                if not isinstance(field, str):
                    raise TypeError(f'fields must be str, not {type(field).__name__}')
                if field not in FIELDS:
                    raise ValueError(f'fields mus be only {FIELDS}')
        if not isinstance(named_fields, list) and named_fields is not None:
            raise TypeError(f'named_fields must be list with str, not {type(named_fields).__name__}')
        if named_fields is not None:
            for named_field in named_fields:
                if not isinstance(named_field, str):
                    raise TypeError(f'named_field must be str, not {type(named_field).__name__}')
                if named_field not in FIELDS:
                    raise ValueError(f'named_field mus be only {FIELDS}')

    @staticmethod
    def _get_date():
        return datetime.now().date()

    @staticmethod
    def _get_tracback_file():
        for x in traceback.StackSummary.extract(traceback.walk_stack(None)):
            if x.filename != __file__ and x.filename != '<string>':
                return x.filename

    @staticmethod
    def _get_tracback_line():
        return traceback.StackSummary.extract(traceback.walk_stack(None))[-1].lineno
