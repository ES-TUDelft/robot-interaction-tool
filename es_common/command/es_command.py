class ESCommand(object):
    def __init__(self):
        self.id = id(self)

    def reset(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
