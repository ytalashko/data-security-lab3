import datetime
import os


class Logger(object):

    def __init__(self, log_dir_path):
        if not os.path.exists(log_dir_path):
            os.makedirs(log_dir_path)
        self._log_dir_path = log_dir_path

    def info(self, user_name, message):
        self._log('info', user_name, message)

    def error(self, user_name, message):
        self._log('error', user_name, message)

    def _log(self, level, user_name, message):
        file_name = self._get_file_name(level, user_name)
        with open(os.path.join(self._log_dir_path, file_name), 'a') as log_file:
            log_file.write('{} {}: {}\n'.format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                str(level).upper(), message))

    def _get_file_name(self, level, user_name):
        return user_name + ('.error' if str(level).lower() == 'error' else '.log')
