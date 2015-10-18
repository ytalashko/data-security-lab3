from accessible_object import AccessibleObject


class File(AccessibleObject):

    def __init__(self, user_name, name):
        super(File, self).__init__(user_name, name)
        for user in [user_name, 'group', 'all']:
            self.set_right(user, 0, True)
        self.set_right(user_name, 1, True)
        self._data = ''

    def read(self):
        return self._data

    def write(self, data):
        self._data = data

    def execute(self):
        pass

    def delete(self):
        pass
