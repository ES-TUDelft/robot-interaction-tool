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
        ConnectionDialog.resize(420, 453)
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
        self.robotIPLabel = QtWidgets.QLabel(self.groupBox)
        self.robotIPLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.robotIPLabel.setObjectName("robotIPLabel")
        self.gridLayout_12.addWidget(self.robotIPLabel, 1, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.messageTextEdit = QtWidgets.QTextEdit(self.groupBox_2)
        self.messageTextEdit.setAutoFillBackground(True)
        self.messageTextEdit.setStyleSheet("background: rgb(76, 76, 76)")
        self.messageTextEdit.setObjectName("messageTextEdit")
        self.gridLayout_2.addWidget(self.messageTextEdit, 0, 0, 1, 1)
        self.gridLayout_12.addWidget(self.groupBox_2, 5, 0, 1, 3)
        self.portLabel = QtWidgets.QLabel(self.groupBox)
        self.portLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.portLabel.setObjectName("portLabel")
        self.gridLayout_12.addWidget(self.portLabel, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem, 8, 1, 1, 1)
        self.robotPortValue = QtWidgets.QLineEdit(self.groupBox)
        self.robotPortValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.robotPortValue.setObjectName("robotPortValue")
        self.gridLayout_12.addWidget(self.robotPortValue, 2, 1, 1, 2)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_12.addWidget(self.line, 4, 0, 1, 3)
        self.connectPushButton = QtWidgets.QPushButton(self.groupBox)
        self.connectPushButton.setObjectName("connectPushButton")
        self.gridLayout_12.addWidget(self.connectPushButton, 3, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.groupBox)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_12.addWidget(self.buttonBox, 6, 1, 1, 2)
        self.robotIPValue = QtWidgets.QLineEdit(self.groupBox)
        self.robotIPValue.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.robotIPValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.robotIPValue.setObjectName("robotIPValue")
        self.gridLayout_12.addWidget(self.robotIPValue, 1, 1, 1, 2)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout_12.addWidget(self.label, 0, 0, 1, 1)
        self.robotNameComboBox = QtWidgets.QComboBox(self.groupBox)
        self.robotNameComboBox.setObjectName("robotNameComboBox")
        self.robotNameComboBox.addItem("")
        self.robotNameComboBox.addItem("")
        self.gridLayout_12.addWidget(self.robotNameComboBox, 0, 1, 1, 2)
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
        self.robotIPLabel.setText(_translate("ConnectionDialog", "IP"))
        self.groupBox_2.setTitle(_translate("ConnectionDialog", "Log"))
        self.portLabel.setText(_translate("ConnectionDialog", "Port"))
        self.robotPortValue.setPlaceholderText(_translate("ConnectionDialog", "9559"))
        self.connectPushButton.setText(_translate("ConnectionDialog", "Connect"))
        self.robotIPValue.setPlaceholderText(_translate("ConnectionDialog", "127.0.0.0"))
        self.label.setText(_translate("ConnectionDialog", "Name"))
        self.robotNameComboBox.setItemText(0, _translate("ConnectionDialog", "Pepper"))
        self.robotNameComboBox.setItemText(1, _translate("ConnectionDialog", "Nao"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConnectionDialog = QtWidgets.QDialog()
    ui = Ui_ConnectionDialog()
    ui.setupUi(ConnectionDialog)
    ConnectionDialog.show()
    sys.exit(app.exec_())
