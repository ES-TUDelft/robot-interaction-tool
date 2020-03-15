import time

from PyQt5 import QtWidgets, QtCore, QtGui
import logging

from PyQt5.QtCore import QTimer

from es_common.model.observable import Observable


class SimulationController(object):
    def __init__(self, block_controller, parent=None):

        self.logger = logging.getLogger("SimulationController")
        self.block_controller = block_controller
        self.user_input = None
        self.interaction_log = None
        self.simulation_dock_widget = None
        self._init_dock_widget(parent)
        self.user_turn = False

        self.current_interaction_block = None
        self.previous_interaction_block = None
        self.connecting_edge = None
        self.execution_result = None
        self.stop_playing = False
        self.finished_simulation_observable = Observable()

    def _init_dock_widget(self, parent):
        self.simulation_dock_widget = QtWidgets.QDockWidget("Simulation", parent)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.simulation_dock_widget.sizePolicy().hasHeightForWidth())
        self.simulation_dock_widget.setSizePolicy(size_policy)
        self.simulation_dock_widget.setMinimumSize(QtCore.QSize(98, 150))
        self.simulation_dock_widget.setFloating(False)
        self.simulation_dock_widget.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.simulation_dock_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.simulation_dock_widget.setObjectName("simulationDockWidget")
        # layout
        widget_content = QtWidgets.QWidget()
        widget_content.setObjectName("simulationDockWidgetContents")
        grid_layout = QtWidgets.QGridLayout(widget_content)
        grid_layout.setContentsMargins(11, 11, 11, 11)
        grid_layout.setSpacing(6)
        grid_layout.setObjectName("simulationGridLayout")
        # display text edit
        self.interaction_log = QtWidgets.QTextEdit(widget_content)
        self.interaction_log.setAcceptDrops(False)
        self.interaction_log.setAutoFillBackground(True)
        self.interaction_log.setStyleSheet("background: white")
        self.interaction_log.setUndoRedoEnabled(False)
        self.interaction_log.setReadOnly(True)
        self.interaction_log.setAcceptRichText(True)
        self.interaction_log.setObjectName("simulationTextEdit")
        grid_layout.addWidget(self.interaction_log, 0, 0, 1, 1)
        # user input
        self.user_input = QtWidgets.QLineEdit(widget_content)
        self.user_input.setPlaceholderText("User Input")
        self.user_input.returnPressed.connect(lambda: self.update_interaction_log(user_message=self.user_input.text()))
        self.user_input.setObjectName("simulationLineEdit")
        grid_layout.addWidget(self.user_input, 1, 0, 1, 1)

        widget_content.setLayout(grid_layout)
        self.simulation_dock_widget.setWidget(widget_content)

    def reset(self):
        self.block_controller.clear_selection()
        self.interaction_log.clear()
        self.user_turn = False
        self.current_interaction_block = None
        self.previous_interaction_block = None
        self.connecting_edge = None
        self.execution_result = None
        self.stop_playing = False

    def start_simulation(self, int_block):
        if int_block is None:
            return

        self.reset()

        self.current_interaction_block = int_block
        self.execute_next_interaction_block()

    def execute_next_interaction_block(self):
        self.logger.debug("Getting the next interaction block...")
        if self.current_interaction_block is None \
                or self.user_turn is True:
            return

        self.logger.debug("Execution Result: {}".format(self.execution_result))

        if self.previous_interaction_block is None:  # simulation just started
            # update previous block only
            self.previous_interaction_block = self.current_interaction_block
        else:  # update previous and next blocks
            self.previous_interaction_block = self.current_interaction_block
            self.current_interaction_block, self.connecting_edge = \
                self.current_interaction_block.get_next_interaction_block(execution_result=self.execution_result)
            # reset execution_result
            self.execution_result = None

        self.simulate_interaction()

    def simulate_interaction(self):
        self.block_controller.clear_selection()

        # if there are no more blocks, stop interacting
        if self.current_interaction_block is None or self.stop_playing is True:
            self.update_interaction_log(robot_message="Finished the interaction!")
            self.finished_simulation_observable.notify_all(True)
            return True
        else:
            # execute the block
            self.logger.debug("Executing: {}".format(self.current_interaction_block.name))
            self.current_interaction_block.set_selected(True)
            if self.connecting_edge is not None:
                self.connecting_edge.set_selected(True)

            self.update_interaction_log(robot_message=self.current_interaction_block.message)

            if self.current_interaction_block.topic_tag.topic != "":
                self.user_turn = True
            else:
                QTimer.singleShot(1000, self.execute_next_interaction_block)

    def check_robot_feedback(self):
        if self.current_interaction_block is None or self.execution_result is None:
            return self.execute_next_interaction_block()
        try:
            for i in range(len(self.current_interaction_block.topic_tag.answers)):
                # if the result is in the answers ==> go to appropriate interaction block
                if self.execution_result.lower() in self.current_interaction_block.topic_tag.answers[i].lower():
                    self.update_interaction_log(robot_message=self.current_interaction_block.topic_tag.feedbacks[i])
        except Exception as e:
            self.logger.error("Error while logging the feedback! {}".format(e))
        finally:
            QTimer.singleShot(1500, self.execute_next_interaction_block)

    def update_interaction_log(self, robot_message=None, user_message=None):
        if robot_message is not None:
            self._append_interaction_text(name="Robot", color_name="green", message=robot_message)
        elif self.user_turn is True:  # user_input is not None
            # to prevent logging users' entered input when it's not their turn
            self._append_interaction_text(name="User", color_name="maroon", message=user_message)

            # clear input and continue
            self.user_input.clear()
            self.user_turn = False
            self.execution_result = user_message
            self.check_robot_feedback()

    def _append_interaction_text(self, name, color_name, message):
        self.interaction_log.setTextColor(QtGui.QColor(color_name))
        self.interaction_log.append("{}:".format(name))
        self.interaction_log.setTextColor(QtGui.QColor("black"))
        self.interaction_log.append("{}".format(message))

        self.logger.debug("{}: {}".format(name, message))