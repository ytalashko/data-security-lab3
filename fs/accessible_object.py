import abc


class AccessibleObject(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, user_name, name):
        self._right = {user_name: [False] * 3,
                       'group': [False] * 3,
                       'all': [False] * 3}
        self._name = name

    @property
    def right(self):
        return self._right

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
