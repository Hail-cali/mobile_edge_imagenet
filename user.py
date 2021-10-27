


class User:

    def __init__(self, user=None):
        self.size = 0
        self.backward = None
        self.user = user
        self.forward = None

    @property
    def next(self):
        return self.forward

    @property
    def previous(self):
        return self.backward

