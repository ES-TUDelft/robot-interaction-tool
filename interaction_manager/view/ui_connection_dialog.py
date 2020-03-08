# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interaction_manager/ui/connectiondialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConnectionDialog(object):
    def setupUi(self, ConnectionDialog):
        ConnectionDialog.setObjectName("ConnectionDialog")
        ConnectionDialog.resize(399, 360)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ConnectionDialog.sizePolicy().hasHeightForWidth())
        ConnectionDialog.setSizePolicy(sizePolicy)
        ConnectionDialog.setMinimumSize(QtCore.QSize(350, 220))
        ConnectionDialog.setMaximumSize(QtCore.QSize(500, 500))
        self.gridLayout_3 = QtWidgets.QGridLayout(ConnectionDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(ConnectionDialog)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.portLabel = QtWidgets.QLabel(self.groupBox)
        self.portLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.portLabel.setObjectName("portLabel")
        self.gridLayout_12.addWidget(self.portLabel, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.groupBox)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_12.addWidget(self.buttonBox, 5, 1, 1, 2)
        self.robotPortValue = QtWidgets.QLineEdit(self.groupBox)
        self.robotPortValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.robotPortValue.setObjectName("robotPortValue")
        self.gridLayout_12.addWidget(self.robotPortValue, 1, 1, 1, 2)
        self.robotIPLabel = QtWidgets.QLabel(self.groupBox)
        self.robotIPLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.robotIPLabel.setObjectName("robotIPLabel")
        self.gridLayout_12.addWidget(self.robotIPLabel, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_12.addWidget(self.line, 3, 0, 1, 3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.messageTextEdit = QtWidgets.QTextEdit(self.groupBox_2)
        self.messageTextEdit.setAutoFillBackground(True)
        self.messageTextEdit.setStyleSheet("background: rgb(76, 76, 76)")
        self.messageTextEdit.setObjectName("messageTextEdit")
        self.gridLayout_2.addWidget(self.messageTextEdit, 0, 0, 1, 1)
        self.gridLayout_12.addWidget(self.groupBox_2, 4, 0, 1, 3)
        self.robotIPValue = QtWidgets.QLineEdit(self.groupBox)
        self.robotIPValue.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.robotIPValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.robotIPValue.setObjectName("robotIPValue")
        self.gridLayout_12.addWidget(self.robotIPValue, 0, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem, 7, 1, 1, 1)
        self.connectPushButton = QtWidgets.QPushButton(self.groupBox)
        self.connectPushButton.setObjectName("connectPushButton")
        self.gridLayout_12.addWidget(self.connectPushButton, 2, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_12, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(ConnectionDialog)
        self.buttonBox.accepted.connect(ConnectionDialog.accept)
        self.buttonBox.rejected.connect(ConnectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConnectionDialog)

    def retranslateUi(self, ConnectionDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectionDialog.setWindowTitle(_translate("ConnectionDialog", "Connection Dialog"))
        self.groupBox.setTitle(_translate("ConnectionDialog", "Robot"))
        self.portLabel.setText(_translate("ConnectionDialog", "Port"))
        self.robotPortValue.setPlaceholderText(_translate("ConnectionDialog", "9559"))
        self.robotIPLabel.setText(_translate("ConnectionDialog", "IP"))
        self.groupBox_2.setTitle(_translate("ConnectionDialog", "Log"))
        self.robotIPValue.setPlaceholderText(_translate("ConnectionDialog", "127.0.0.0"))
        self.connectPushButton.setText(_translate("ConnectionDialog", "Connect"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConnectionDialog = QtWidgets.QDialog()
    ui = Ui_ConnectionDialog()
    ui.setupUi(ConnectionDialog)
    ConnectionDialog.show()
    sys.exit(app.exec_())
