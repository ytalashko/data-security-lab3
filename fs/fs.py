import json
import os
import random
import re
import string

from directory import Directory
from file import File
from logger.logger import Logger


class FileSystem():

    def __init__(self):
        self._users = self._get_users()
        self._current_user = None
        self._topology = self._generate_topology()
        self._logger = Logger.default_logger()

    def login(self, user_name, password, x, y):
        user = self._users.get(user_name)
        if user and user['pass'] == password and user['captcha'](x, y):
            self._current_user = user_name
            return True
        return False

    def logged(self):
        return self._current_user is not None

    def logout(self):
        self._current_user = None

    def check_captcha(self, x, y):
        return self._users[self._current_user]['captcha'](x, y)

    def read(self, path):
        ao = self._get_accessible_object(path)
        if ao:
            if self._check_right(ao, 0):
                self._logger.info(self._current_user,
                                  "Read action on {}".format(path))
                return ao.read()
            else:
                self._logger.error(self._current_user,
                                   "Read action on {}: "
                                   "Access denied".format(path))
        return None

    def write(self, path, data):
        ao = self._get_accessible_object(path)
        if ao:
            if self._check_right(ao, 1):
                self._logger.info(self._current_user,
                                  "Write action to {}".format(path))
                ao.write(data)
                return True
            else:
                self._logger.error(self._current_user,
                                   "Write action to {}: "
                                   "Access denied".format(path))
        return False

    def execute(self, path):
        ao = self._get_accessible_object(path)
        if ao:
            if self._check_right(ao, 2):
                self._logger.info(self._current_user,
                                  "Execute action on {}".format(path))
                ao.execute()
                return True
            else:
                self._logger.error(self._current_user,
                                   "Execute action on {}: "
                                   "Access denied".format(path))
        return False

    def delete(self, path):
        ao = self._get_accessible_object(path)
        if ao:
            if self._check_right(ao, 1):
                self._logger.info(self._current_user,
                                  "Delete action on {}".format(path))
                ao.delete()
                self._delete_accessible_object(path)
                return True
            else:
                self._logger.error(self._current_user,
                                   "Delete action on {}: "
                                   "Access denied".format(path))
        return False

    def _check_right(self, ao, index):
        return ao.right['all'][index] or ao.right.get(
            self._current_user, [False] * 3)[index]

    # Do not checks for right path
    def _delete_accessible_object(self, ao_path):
        path = str(ao_path).split("/")
        current_ao = self._get_by_name(self._topology, path[0])
        for ao_name in path[1:-1]:
            current_ao = self._get_by_name(current_ao.read(), ao_name)
        # Dirty hack
        current_ao.data.read()[:] = [e for e in current_ao.data.read()
                                     if e.name != path[-1]]

    def _get_accessible_object(self, ao_path):
        path = str(ao_path).split("/")
        current_ao = self._get_by_name(self._topology, path[0])
        for ao_name in path[1:]:
            if type(current_ao) is File:
                return None
            current_ao = self._get_by_name(current_ao.read(), ao_name)
        return current_ao

    def _get_by_name(self, data, name):
        for ao in data:
            if ao.name == name:
                return ao
        return None

    def _get_users(self, file_path=None):
        if not file_path:
            file_path = os.path.join(os.path.dirname(__file__),
                                     'resources', 'users.json')
        json_array = json.load(file(file_path))
        users = dict()
        for json_object in json_array:
            users[json_object['login']] = {
                'pass': json_object['password'],
                'captcha': self._parse_captcha(json_object['captcha'])
            }
        return users

    # TODO: add parsing for expressions with brackets
    # TODO: doesn't work with negative numbers, refers to the above TODO)
    # TODO: improve this (+clean up)
    def _parse_captcha(self, captcha):
        captcha = str(captcha).replace(' ', '')

        def check(x, y):
            expression = re.sub('[A-Za-z]', str(x), captcha)
            while True:
                pattern = '.*?(\d+(?:\.\d+)?)([*/^])(\d+(?:\.\d+)?)'
                match_object = re.match(pattern, expression)
                if match_object:
                    left_arg = float(match_object.group(1))
                    right_arg = float(match_object.group(3))
                    operation = match_object.group(2)
                    if operation == '*':
                        result = left_arg * right_arg
                    elif operation == '/':
                        result = left_arg / right_arg
                    else:
                        result = left_arg ** right_arg
                else:
                    pattern = '.*?(\d+(?:\.\d+)?)([+-])(\d+(?:\.\d+)?)'
                    match_object = re.match(pattern, expression)
                    if match_object:
                        left_arg = float(match_object.group(1))
                        right_arg = float(match_object.group(3))
                        operation = match_object.group(2)
                        if operation == '+':
                            result = left_arg + right_arg
                        else:
                            result = left_arg - right_arg
                    else:
                        return float(y) == float(expression)
                expression = re.sub(pattern[3:], str(result),
                                    expression, count=1)
        return check

    def _generate_topology(self, width=7, depth=7):
        if depth > 0:
            topology = list()
            for i in range(0, width):
                isFile = random.choice([True, False])
                user_name = random.choice(self._users.keys())
                name = ''.join(random.choice(string.lowercase)
                               for _ in range(random.randint(7, 14)))
                if isFile:
                    topology.append(File(user_name, name))
                else:
                    directory = Directory(user_name, name)
                    directory_data = self._generate_topology(width=width,
                                                             depth=depth-1)
                    if directory_data:
                        for accessible_object in directory_data:
                            directory.write(accessible_object)
                    topology.append(directory)
            return topology
        return None
