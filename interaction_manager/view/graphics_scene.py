from __future__ import absolute_import

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from interaction_manager.utils import config_helper
import math
import logging


class ESGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super(ESGraphicsScene, self).__init__(parent)

        self.logger = logging.getLogger("GraphicsScene")

        self.scene = scene

        # properties
        self.grid_size = 20
        self.grid_squares = 5

        block_colors = config_helper.get_colors()
        self._light_pen = QPen(QColor("#{}".format(block_colors['pen']['light'])))
        self._dark_pen = QPen(QColor("#{}".format(block_colors['pen']['dark'])))
        # set pen width
        self._light_pen.setWidth(1)
        self._dark_pen.setWidth(2)

        self.setBackgroundBrush(QColor("#{}".format(block_colors['brush']['scene_bg'])))

    # override to allow drag
    def dragMoveEvent(self, event):
        pass

    def set_scene_rect(self, width, height):
        self.setSceneRect(-width // 2, -height // 2,
                          width, height)

    def drawBackground(self, painter, rect):
        super(ESGraphicsScene, self).drawBackground(painter, rect)

        try:
            light_lines, dark_lines = (None, ) * 2  # self.create_grid_lines(rect, self.grid_size, self.grid_squares)

            # draw lines
            if light_lines is not None and len(light_lines) > 0:
                painter.setPen(self._light_pen)
                painter.drawLines(*light_lines)
            if dark_lines is not None and len(dark_lines) > 0:
                painter.setPen(self._dark_pen)
                painter.drawLines(*dark_lines)
        except Exception as e:
            self.logger.error("Error while drawing the grid. {}".format(e))

    def create_grid_lines(self, rect, grid_size, num_of_squares):
        _left = int(math.floor(rect.left()))
        _right = int(math.ceil(rect.right()))
        _top = int(math.floor(rect.top()))
        _bottom = int(math.ceil(rect.bottom()))

        first_left = _left - (_left % grid_size)
        first_top = _top - (_top % grid_size)

        light_lines = []
        dark_lines = []

        for x in range(first_left, _right, grid_size):
            if x % (grid_size * num_of_squares) != 0:
                light_lines.append(QLine(x, _top, x, _bottom))
            else:
                dark_lines.append(QLine(x, _top, x, _bottom))

        for y in range(first_top, _bottom, grid_size):
            if y % (grid_size * num_of_squares) != 0:
                light_lines.append(QLine(_left, y, _right, y))
            else:
                dark_lines.append(QLine(_left, y, _right, y))

        return light_lines, dark_lines
