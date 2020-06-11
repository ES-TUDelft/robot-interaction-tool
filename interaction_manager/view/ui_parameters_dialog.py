# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interaction_manager/ui/parametersdialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ParametersDialog(object):
    def setupUi(self, ParametersDialog):
        ParametersDialog.setObjectName("ParametersDialog")
        ParametersDialog.resize(449, 526)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ParametersDialog.sizePolicy().hasHeightForWidth())
        ParametersDialog.setSizePolicy(sizePolicy)
        ParametersDialog.setMinimumSize(QtCore.QSize(0, 0))
        ParametersDialog.setMaximumSize(QtCore.QSize(1000, 1000))
        self.gridLayout_2 = QtWidgets.QGridLayout(ParametersDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(ParametersDialog)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scrollArea.setLineWidth(1)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 405, 458))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.parametersTabWidget = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
        self.parametersTabWidget.setObjectName("parametersTabWidget")
        self.nonVerbalParameters = QtWidgets.QWidget()
        self.nonVerbalParameters.setObjectName("nonVerbalParameters")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.nonVerbalParameters)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.line_3 = QtWidgets.QFrame(self.nonVerbalParameters)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_17.addWidget(self.line_3, 3, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.nonVerbalParameters)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_17.addWidget(self.line_4, 5, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.whiteEyeColorRadioButton = QtWidgets.QRadioButton(self.nonVerbalParameters)
        self.whiteEyeColorRadioButton.setChecked(True)
        self.whiteEyeColorRadioButton.setObjectName("whiteEyeColorRadioButton")
        self.gridLayout_4.addWidget(self.whiteEyeColorRadioButton, 0, 2, 1, 1)
        self.redEyeColorRadioButton = QtWidgets.QRadioButton(self.nonVerbalParameters)
        self.redEyeColorRadioButton.setObjectName("redEyeColorRadioButton")
        self.gridLayout_4.addWidget(self.redEyeColorRadioButton, 0, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.nonVerbalParameters)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(65, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        self.blueEyeColorRadioButton = QtWidgets.QRadioButton(self.nonVerbalParameters)
        self.blueEyeColorRadioButton.setObjectName("blueEyeColorRadioButton")
        self.gridLayout_4.addWidget(self.blueEyeColorRadioButton, 1, 3, 1, 1)
        self.greenEyeColorRadioButton = QtWidgets.QRadioButton(self.nonVerbalParameters)
        self.greenEyeColorRadioButton.setObjectName("greenEyeColorRadioButton")
        self.gridLayout_4.addWidget(self.greenEyeColorRadioButton, 1, 2, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.nonVerbalParameters)
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout_4.addWidget(self.line_9, 0, 1, 2, 1)
        self.gridLayout_17.addLayout(self.gridLayout_4, 6, 0, 1, 1)
        self.gridLayout_28 = QtWidgets.QGridLayout()
        self.gridLayout_28.setObjectName("gridLayout_28")
        self.label_12 = QtWidgets.QLabel(self.nonVerbalParameters)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_28.addWidget(self.label_12, 0, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.nonVerbalParameters)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(65, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_28.addWidget(self.label_7, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_28.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_28.addItem(spacerItem1, 0, 6, 1, 1)
        self.line_6 = QtWidgets.QFrame(self.nonVerbalParameters)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout_28.addWidget(self.line_6, 0, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.nonVerbalParameters)
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_28.addWidget(self.label_13, 0, 5, 1, 1)
        self.gazePatternSlider = QtWidgets.QSlider(self.nonVerbalParameters)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gazePatternSlider.sizePolicy().hasHeightForWidth())
        self.gazePatternSlider.setSizePolicy(sizePolicy)
        self.gazePatternSlider.setMaximum(1)
        self.gazePatternSlider.setPageStep(1)
        self.gazePatternSlider.setProperty("value", 0)
        self.gazePatternSlider.setSliderPosition(0)
        self.gazePatternSlider.setOrientation(QtCore.Qt.Horizontal)
        self.gazePatternSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.gazePatternSlider.setObjectName("gazePatternSlider")
        self.gridLayout_28.addWidget(self.gazePatternSlider, 0, 4, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_28, 2, 0, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.nonVerbalParameters)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_17.addWidget(self.line_5, 7, 0, 1, 1)
        self.gridLayout_25 = QtWidgets.QGridLayout()
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.proxemicsLcdNumber = QtWidgets.QLCDNumber(self.nonVerbalParameters)
        self.proxemicsLcdNumber.setEnabled(True)
        self.proxemicsLcdNumber.setAutoFillBackground(False)
        self.proxemicsLcdNumber.setStyleSheet("background-color: rgb(204, 204, 204);")
        self.proxemicsLcdNumber.setFrameShape(QtWidgets.QFrame.Panel)
        self.proxemicsLcdNumber.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.proxemicsLcdNumber.setLineWidth(1)
        self.proxemicsLcdNumber.setSmallDecimalPoint(True)
        self.proxemicsLcdNumber.setProperty("value", 3.5)
        self.proxemicsLcdNumber.setObjectName("proxemicsLcdNumber")
        self.gridLayout_25.addWidget(self.proxemicsLcdNumber, 1, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.nonVerbalParameters)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(65, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_25.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.nonVerbalParameters)
        self.label_5.setObjectName("label_5")
        self.gridLayout_25.addWidget(self.label_5, 0, 2, 1, 1)
        self.proxemicsSlider = QtWidgets.QSlider(self.nonVerbalParameters)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.proxemicsSlider.sizePolicy().hasHeightForWidth())
        self.proxemicsSlider.setSizePolicy(sizePolicy)
        self.proxemicsSlider.setMinimum(0)
        self.proxemicsSlider.setMaximum(10)
        self.proxemicsSlider.setPageStep(1)
        self.proxemicsSlider.setProperty("value", 5)
        self.proxemicsSlider.setSliderPosition(5)
        self.proxemicsSlider.setOrientation(QtCore.Qt.Horizontal)
        self.proxemicsSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.proxemicsSlider.setTickInterval(2)
        self.proxemicsSlider.setObjectName("proxemicsSlider")
        self.gridLayout_25.addWidget(self.proxemicsSlider, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.nonVerbalParameters)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_25.addWidget(self.label_4, 0, 4, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.nonVerbalParameters)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout_25.addWidget(self.line_8, 0, 1, 2, 1)
        self.gridLayout_17.addLayout(self.gridLayout_25, 4, 0, 1, 1)
        self.gridLayout_24 = QtWidgets.QGridLayout()
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.label_3 = QtWidgets.QLabel(self.nonVerbalParameters)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_24.addWidget(self.label_3, 0, 5, 1, 1)
        self.gestureOpennessSlider = QtWidgets.QSlider(self.nonVerbalParameters)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gestureOpennessSlider.sizePolicy().hasHeightForWidth())
        self.gestureOpennessSlider.setSizePolicy(sizePolicy)
        self.gestureOpennessSlider.setMinimum(0)
        self.gestureOpennessSlider.setMaximum(1)
        self.gestureOpennessSlider.setPageStep(1)
        self.gestureOpennessSlider.setProperty("value", 0)
        self.gestureOpennessSlider.setOrientation(QtCore.Qt.Horizontal)
        self.gestureOpennessSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.gestureOpennessSlider.setObjectName("gestureOpennessSlider")
        self.gridLayout_24.addWidget(self.gestureOpennessSlider, 0, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_24.addItem(spacerItem2, 0, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.nonVerbalParameters)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_24.addWidget(self.label_10, 0, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_24.addItem(spacerItem3, 0, 6, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.nonVerbalParameters)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(65, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_24.addWidget(self.label_2, 0, 0, 1, 1)
        self.line_7 = QtWidgets.QFrame(self.nonVerbalParameters)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout_24.addWidget(self.line_7, 0, 1, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_24, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.nonVerbalParameters)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_17.addWidget(self.line, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_17, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 1, 0, 1, 1)
        self.parametersTabWidget.addTab(self.nonVerbalParameters, "")
        self.voiceParameters = QtWidgets.QWidget()
        self.voiceParameters.setObjectName("voiceParameters")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.voiceParameters)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.groupBox_9 = QtWidgets.QGroupBox(self.voiceParameters)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_9.setFont(font)
        self.groupBox_9.setObjectName("groupBox_9")
        self.gridLayout_29 = QtWidgets.QGridLayout(self.groupBox_9)
        self.gridLayout_29.setObjectName("gridLayout_29")
        self.gridLayout_30 = QtWidgets.QGridLayout()
        self.gridLayout_30.setObjectName("gridLayout_30")
        self.label_21 = QtWidgets.QLabel(self.groupBox_9)
        self.label_21.setObjectName("label_21")
        self.gridLayout_30.addWidget(self.label_21, 3, 4, 1, 1)
        self.voiceProsodySlider = QtWidgets.QSlider(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voiceProsodySlider.sizePolicy().hasHeightForWidth())
        self.voiceProsodySlider.setSizePolicy(sizePolicy)
        self.voiceProsodySlider.setMinimum(0)
        self.voiceProsodySlider.setMaximum(1)
        self.voiceProsodySlider.setSingleStep(1)
        self.voiceProsodySlider.setPageStep(1)
        self.voiceProsodySlider.setProperty("value", 0)
        self.voiceProsodySlider.setOrientation(QtCore.Qt.Horizontal)
        self.voiceProsodySlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.voiceProsodySlider.setTickInterval(1)
        self.voiceProsodySlider.setObjectName("voiceProsodySlider")
        self.gridLayout_30.addWidget(self.voiceProsodySlider, 5, 2, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBox_9)
        self.label_18.setObjectName("label_18")
        self.gridLayout_30.addWidget(self.label_18, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_9)
        self.label_6.setObjectName("label_6")
        self.gridLayout_30.addWidget(self.label_6, 1, 4, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox_9)
        self.label_15.setObjectName("label_15")
        self.gridLayout_30.addWidget(self.label_15, 1, 0, 1, 1)
        self.voiceSpeedSlider = QtWidgets.QSlider(self.groupBox_9)
        self.voiceSpeedSlider.setMinimum(-4)
        self.voiceSpeedSlider.setMaximum(4)
        self.voiceSpeedSlider.setPageStep(1)
        self.voiceSpeedSlider.setOrientation(QtCore.Qt.Horizontal)
        self.voiceSpeedSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.voiceSpeedSlider.setTickInterval(2)
        self.voiceSpeedSlider.setObjectName("voiceSpeedSlider")
        self.gridLayout_30.addWidget(self.voiceSpeedSlider, 3, 1, 1, 3)
        self.voiceSpeedLabel = QtWidgets.QLabel(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voiceSpeedLabel.sizePolicy().hasHeightForWidth())
        self.voiceSpeedLabel.setSizePolicy(sizePolicy)
        self.voiceSpeedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.voiceSpeedLabel.setObjectName("voiceSpeedLabel")
        self.gridLayout_30.addWidget(self.voiceSpeedLabel, 2, 1, 1, 3)
        self.voicePitchSlider = QtWidgets.QSlider(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voicePitchSlider.sizePolicy().hasHeightForWidth())
        self.voicePitchSlider.setSizePolicy(sizePolicy)
        self.voicePitchSlider.setMinimum(-4)
        self.voicePitchSlider.setMaximum(4)
        self.voicePitchSlider.setSingleStep(1)
        self.voicePitchSlider.setPageStep(1)
        self.voicePitchSlider.setProperty("value", 0)
        self.voicePitchSlider.setOrientation(QtCore.Qt.Horizontal)
        self.voicePitchSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.voicePitchSlider.setTickInterval(2)
        self.voicePitchSlider.setObjectName("voicePitchSlider")
        self.gridLayout_30.addWidget(self.voicePitchSlider, 1, 1, 1, 3)
        self.voicePitchLabel = QtWidgets.QLabel(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voicePitchLabel.sizePolicy().hasHeightForWidth())
        self.voicePitchLabel.setSizePolicy(sizePolicy)
        self.voicePitchLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.voicePitchLabel.setObjectName("voicePitchLabel")
        self.gridLayout_30.addWidget(self.voicePitchLabel, 0, 1, 1, 3)
        self.label_16 = QtWidgets.QLabel(self.groupBox_9)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_30.addWidget(self.label_16, 4, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_30.addItem(spacerItem5, 4, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_30.addItem(spacerItem6, 4, 3, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.groupBox_9)
        self.label_17.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout_30.addWidget(self.label_17, 5, 0, 1, 2)
        self.label_22 = QtWidgets.QLabel(self.groupBox_9)
        self.label_22.setObjectName("label_22")
        self.gridLayout_30.addWidget(self.label_22, 5, 3, 1, 2)
        self.gridLayout_29.addLayout(self.gridLayout_30, 0, 0, 1, 1)
        self.gridLayout_18.addWidget(self.groupBox_9, 0, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_18.addItem(spacerItem7, 1, 0, 1, 1)
        self.parametersTabWidget.addTab(self.voiceParameters, "")
        self.verticalLayout.addWidget(self.parametersTabWidget)
        self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.gridLayout_32 = QtWidgets.QGridLayout()
        self.gridLayout_32.setObjectName("gridLayout_32")
        self.behavioralParametersApplyToAllButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.behavioralParametersApplyToAllButton.setObjectName("behavioralParametersApplyToAllButton")
        self.gridLayout_32.addWidget(self.behavioralParametersApplyToAllButton, 0, 1, 1, 1)
        self.warningLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setItalic(True)
        self.warningLabel.setFont(font)
        self.warningLabel.setStyleSheet("color: rgb(236, 236, 236);")
        self.warningLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.warningLabel.setObjectName("warningLabel")
        self.gridLayout_32.addWidget(self.warningLabel, 1, 0, 1, 2)
        self.testBehavioralParametersButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.testBehavioralParametersButton.setEnabled(False)
        self.testBehavioralParametersButton.setObjectName("testBehavioralParametersButton")
        self.gridLayout_32.addWidget(self.testBehavioralParametersButton, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_32)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        self.gridLayout_14.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ParametersDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ParametersDialog)
        self.parametersTabWidget.setCurrentIndex(0)
        self.buttonBox.rejected.connect(ParametersDialog.reject)
        self.buttonBox.accepted.connect(ParametersDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(ParametersDialog)

    def retranslateUi(self, ParametersDialog):
        _translate = QtCore.QCoreApplication.translate
        ParametersDialog.setWindowTitle(_translate("ParametersDialog", "Edit Parameters"))
        self.whiteEyeColorRadioButton.setText(_translate("ParametersDialog", "White"))
        self.redEyeColorRadioButton.setText(_translate("ParametersDialog", "Red"))
        self.label.setText(_translate("ParametersDialog", "Eye Color"))
        self.blueEyeColorRadioButton.setText(_translate("ParametersDialog", "Blue"))
        self.greenEyeColorRadioButton.setText(_translate("ParametersDialog", "Green"))
        self.label_12.setText(_translate("ParametersDialog", "Fixated"))
        self.label_7.setText(_translate("ParametersDialog", "Gaze"))
        self.label_13.setText(_translate("ParametersDialog", "Diverted"))
        self.label_8.setText(_translate("ParametersDialog", "Proxemics"))
        self.label_5.setText(_translate("ParametersDialog", "Close"))
        self.label_4.setText(_translate("ParametersDialog", "Far"))
        self.label_3.setText(_translate("ParametersDialog", "Open"))
        self.label_10.setText(_translate("ParametersDialog", "Close"))
        self.label_2.setText(_translate("ParametersDialog", "Gestures"))
        self.parametersTabWidget.setTabText(self.parametersTabWidget.indexOf(self.nonVerbalParameters), _translate("ParametersDialog", "Behaviors"))
        self.groupBox_9.setTitle(_translate("ParametersDialog", "Voice"))
        self.label_21.setText(_translate("ParametersDialog", "Fast"))
        self.label_18.setText(_translate("ParametersDialog", "Slow"))
        self.label_6.setText(_translate("ParametersDialog", "High"))
        self.label_15.setText(_translate("ParametersDialog", "Low"))
        self.voiceSpeedLabel.setText(_translate("ParametersDialog", "Speed"))
        self.voicePitchLabel.setText(_translate("ParametersDialog", "Pitch"))
        self.label_16.setText(_translate("ParametersDialog", "Prosody"))
        self.label_17.setText(_translate("ParametersDialog", "Weak"))
        self.label_22.setText(_translate("ParametersDialog", "Strong"))
        self.parametersTabWidget.setTabText(self.parametersTabWidget.indexOf(self.voiceParameters), _translate("ParametersDialog", "Voice"))
        self.behavioralParametersApplyToAllButton.setText(_translate("ParametersDialog", "Apply to All"))
        self.warningLabel.setText(_translate("ParametersDialog", "The parameters are modified."))
        self.testBehavioralParametersButton.setText(_translate("ParametersDialog", "Test"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ParametersDialog = QtWidgets.QDialog()
    ui = Ui_ParametersDialog()
    ui.setupUi(ParametersDialog)
    ParametersDialog.show()
    sys.exit(app.exec_())