import traceback
from datetime import datetime


class Logger:

    def __init__(self, log_file='log_file.txt'):
        self.log_file = log_file

    def save_error(self, error):
        time = datetime.now()
        error_doc = error.__doc__
        file_name = traceback.StackSummary.extract(traceback.walk_stack(None))[1].filename
        with open(self.log_file, 'a') as log_file:
            log_file.write(f'[{time}], File: "{file_name}", Error: {error_doc}')

