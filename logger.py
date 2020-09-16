import traceback
from datetime import datetime
import time


class Logger:

    def __init__(self, log_file='log_file.txt'):
        self.log_file = log_file
        self.time = time.localtime()

    def save_error(self, error):
        current_time = self._get_time()
        date = self._get_date()
        error_doc = error.__doc__
        file_name = traceback.StackSummary.extract(traceback.walk_stack(None))[1].filename
        with open(self.log_file, 'a') as log_file:
            log_file.write(f'[{current_time}][{date}], File: "{file_name}", Error: {error_doc} \n')

    def _get_time(self):
        return time.strftime("%H:%M:%S", self.time)

    def _get_date(self):
        return datetime.now().date()
