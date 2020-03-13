from random import random

from es_common.command.es_command import ESCommand


class DrawNumberCommand(ESCommand):
    def __init__(self, range_min=0, range_max=10):
        super(DrawNumberCommand, self).__init__()
        self._set_range(range_min, range_max)
        self.choices = [i for i in range(range_min, range_max)]
        self.prev_choices = []

    def _set_range(self, range_min, range_max):
        self.range_min = int(range_min)
        self.range_max = int(range_max)

        if self.range_min > self.range_max: # flip
            self.range_min = self.range_max
            self.range_max = self.range_min

    def reset(self):
        self.choices = self.prev_choices
        self.prev_choices = []

    def execute(self):
        if len(self.choices) == 0:
            self.reset()

        draw = random.choice(self.choices)
        self.choices.remove(draw)
        self.prev_choices.append(draw)

        return draw
