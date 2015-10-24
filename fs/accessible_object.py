import abc


class AccessibleObject(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, user_name, name):
        self._user_name = user_name
        self._right = {user_name: [False] * 3,
                       'group': [False] * 3,
                       'all': [False] * 3}
        self._name = name

    @property
    def right(self):
        return self._right

    @property
    def ao_right(self):
        # One more hack
        result = ''
        for u in [self._user_name, 'group', 'all']:
            temp_r = 0
            if self._right[u][0]:
                temp_r += 4
            if self._right[u][1]:
                temp_r += 2
            if self._right[u][2]:
                temp_r += 1
            result += str(temp_r)
        return result

    @property
    def user_name(self):
        return self._user_name

    @property
    def name(self):
        return self._name
    
    @abc.abstractmethod
    def read(self):
        pass

    @abc.abstractmethod
    def write(self, data):
        pass

    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def delete(self):
        pass

    def set_right(self, user, index, value):
        self._right[user][index] = value
