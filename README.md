# loger

This package is for logging some errors on python.
Thanks for checking it out.

## Documentation

This is example how to use my package
```python
  import logger

  my_logger = logger.Logger()

  try:
      4 / 0
  except Exception as err:
      my_logger.save_error(err)
```
This code save string:
```
[21:16:53] [2020-09-16] [path/to/file.py] [Second argument to a division or modulo operation was zero.]
```
You can set path to file to save the loggs into:
```python
my_logger = logger.Logger(log_file='path/to/your/lpg/file.txt')
```
The default value of log_file is 'log_file.txt'

You can selct fields for saving to log:

name of field   | value of field
----------------|----------------------
time            | The time of the received error
date            | The date of the received error
file            | The file from which the function is called
error_doc       | The doc of error
line            | The line from which the function is called
exception_name  | The name of the received error

Example
```python
  import logger

  my_logger = logger.Logger(fields=['time', 'error_doc', 'line'])

  try:
      4 / 0
  except Exception as err:
      my_logger.save_error(err)
```
The output will be:
```
[21:20:23] [Second argument to a division or modulo operation was zero.] [8] 
```

You alse can choose field to naming:
```python
  import logger

  my_logger = logger.Logger(fields=['time', 'error_doc', 'line'], named_fields=['time', 'line'])

  try:
      4 / 0
  except Exception as err:
      my_logger.save_error(err)
```
The output of this code will be:
```
[Time: 21:29:46] [Second argument to a division or modulo operation was zero.] [Line: 8] 
```
