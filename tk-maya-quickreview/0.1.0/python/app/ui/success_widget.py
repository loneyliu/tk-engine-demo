# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'success_widget.ui'
#
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_SuccessWidget(object):
    def setupUi(self, SuccessWidget):
        SuccessWidget.setObjectName("SuccessWidget")
        SuccessWidget.resize(552, 166)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SuccessWidget.sizePolicy().hasHeightForWidth())
        SuccessWidget.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QtGui.QGridLayout(SuccessWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.close_btn = QtGui.QPushButton(SuccessWidget)
        self.close_btn.setObjectName("close_btn")
        self.gridLayout.addWidget(self.close_btn, 2, 4, 1, 1)
        self.success_msg = QtGui.QLabel(SuccessWidget)
        self.success_msg.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.success_msg.setObjectName("success_msg")
        self.gridLayout.addWidget(self.success_msg, 1, 2, 1, 3)
        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 5, 4, 1)
        spacerItem1 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 4, 1)
        spacerItem2 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 4)
        spacerItem3 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 3, 1, 1, 4)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 2, 2, 1, 1)
        self.open_btn = QtGui.QPushButton(SuccessWidget)
        self.open_btn.setObjectName("open_btn")
        self.gridLayout.addWidget(self.open_btn, 2, 3, 1, 1)
        self.logo_example = QtGui.QLabel(SuccessWidget)
        self.logo_example.setText("")
        self.logo_example.setPixmap(QtGui.QPixmap(":/res/sg_logo.png"))
        self.logo_example.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.logo_example.setObjectName("logo_example")
        self.gridLayout.addWidget(self.logo_example, 1, 1, 2, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(SuccessWidget)
        QtCore.QMetaObject.connectSlotsByName(SuccessWidget)

    def retranslateUi(self, SuccessWidget):
        SuccessWidget.setWindowTitle(QtGui.QApplication.translate("SuccessWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.close_btn.setText(QtGui.QApplication.translate("SuccessWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.success_msg.setText(QtGui.QApplication.translate("SuccessWidget", "Your review item has been uploaded to a new version in Shotgun!", None, QtGui.QApplication.UnicodeUTF8))
        self.open_btn.setText(QtGui.QApplication.translate("SuccessWidget", "Open in Shotgun", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
from . import resources_rc
