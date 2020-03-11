import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from interaction_manager.utils import config_helper
from interaction_manager.enums.block_enums import Position
import logging

EDGE_CONTROL_POINT_ROUNDNESS = 100


class ESGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super(ESGraphicsEdge, self).__init__(parent)

        self.logger = logging.getLogger("GraphicsEdge")

        self.edge = edge

        # pen
        block_colors = config_helper.get_colors()
        self._pen = QPen(QColor("#{}".format(block_colors['pen']['edge'])))
        self._pen.setWidth(2)
        self._selected_pen = QPen(QColor("#{}".format(block_colors['pen']['edge_selected'])))
        self._selected_pen.setWidthF(4.0)
        self._dragging_pen = QPen(QColor("#{}".format(block_colors['pen']['edge'])))
        self._dragging_pen.setStyle(Qt.DashLine)
        self._dragging_pen.setWidthF(3.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        # z value: make the edge appear behind the block
        self.setZValue(-1)

        self.pos_source = [0, 0]
        self.pos_destination = [100, 300]

    def set_source(self, x, y):
        self.pos_source = [x, y]

    def set_destination(self, x, y):
        self.pos_destination = [x, y]

    # TODO: this was causing segmentation errors!
    # def boundingRect(self):
    #     return self.shape().boundingRect()
    #
    # def shape(self):
    #     return self.compute_path()

    def paint(self, painter, option, widget=None):
        self.update_path()

        painter.setBrush(Qt.NoBrush)

        if self.edge.end_socket is None:
            painter.setPen(self._dragging_pen)
        else:
            painter.setPen(self._selected_pen if self.isSelected() else self._pen)

        painter.drawPath(self.path())

    def update_path(self):
        # updates path from A to B
        path = self.compute_path()
        self.setPath(path)

    def compute_path(self):
        # computes and returns path from A to B
        raise NotImplemented("Abstract method")


class ESGraphicsEdgeDirect(ESGraphicsEdge):
    def compute_path(self):
        path = QPainterPath(QPointF(self.pos_source[0], self.pos_source[1]))
        path.lineTo(self.pos_destination[0], self.pos_destination[1])

        return path


class ESGraphicsEdgeBezier(ESGraphicsEdge):
    def compute_path(self):
        try:
            s = self.pos_source
            d = self.pos_destination
            dist = (d[0] - s[0]) / 2.0

            # set control points
            cpx_s = dist
            cpx_d = -dist
            cpy_s = 0
            cpy_d = 0

            if self.edge.start_socket is not None:
                start_socket_pos = self.edge.start_socket.position
                if (s[0] > d[0] and start_socket_pos in (Position.TOP_RIGHT, Position.BOTTOM_RIGHT)) or \
                        (s[0] < d[0] and start_socket_pos in (Position.BOTTOM_LEFT, Position.TOP_LEFT)):
                    # reverse the distance
                    cpx_d *= -1
                    cpx_s *= -1
                    # avoid division by 0
                    cpy_d = (s[1] - d[1]) / math.fabs(
                        (s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.00001) * EDGE_CONTROL_POINT_ROUNDNESS
                    cpy_s = (d[1] - s[1]) / math.fabs(
                        (d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.00001) * EDGE_CONTROL_POINT_ROUNDNESS
            else:
                self.logger.debug("Edge {} {} has no sockets!".format(type(self), self.edge))

            path = QPainterPath(QPointF(self.pos_source[0], self.pos_source[1]))
            path.cubicTo(
                s[0] + cpx_s, s[1] + cpy_s,
                d[0] + cpx_d, d[1] + cpy_d,  # control points
                self.pos_destination[0], self.pos_destination[1])

            return path
        except Exception as e:
            self.logger.error("ERROR while computing edge path! {}".format(e))
