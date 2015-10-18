from accessible_object import AccessibleObject


class Directory(AccessibleObject):

    def __init__(self, user_name, name):
        super(Directory, self).__init__(user_name, name)
        for user in [user_name, 'group', 'all']:
            for index in [0, 2]:
                self.set_right(user, index, True)
        self.set_right(user_name, 1, True)
        self._data = list()

    def read(self):
        return self._data

    def write(self, data):
        self._data.append(data)

    def execute(self):
        pass

    def delete(self):
        pass
