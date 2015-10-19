class SessionManager(object):

    close_action = None

    def __init__(self, close_action):
        self.close_action = close_action

    def open_session(self):
        self.close_action()
        pass

    def close_session(self):
        pass

    def is_session_opened(self):
        return False

    def refresh_session(self):
        pass
