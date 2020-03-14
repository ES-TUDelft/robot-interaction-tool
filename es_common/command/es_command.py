from es_common.datasource.serializable import Serializable


class ESCommand(Serializable):
    def __init__(self, command_type):
        super(ESCommand, self).__init__()

        self.command_type = command_type

    def clone(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError

    def deserialize(self, data, hashmap={}):
        raise NotImplementedError
