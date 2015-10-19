# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error_widget.ui'
#
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_ErrorWidget(object):
    def setupUi(self, ErrorWidget):
        ErrorWidget.setObjectName("ErrorWidget")
        ErrorWidget.resize(486, 214)
        self.gridLayout_2 = QtGui.QGridLayout(ErrorWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 4, 5, 1)
        self.close_btn = QtGui.QPushButton(ErrorWidget)
        self.close_btn.setObjectName("close_btn")
        self.gridLayout.addWidget(self.close_btn, 3, 3, 1, 1)
        self.error_msg = QtGui.QTextBrowser(ErrorWidget)
        self.error_msg.setObjectName("error_msg")
        self.gridLayout.addWidget(self.error_msg, 2, 2, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 0, 5, 1)
        self.logo_example = QtGui.QLabel(ErrorWidget)
        self.logo_example.setText("")
        self.logo_example.setPixmap(QtGui.QPixmap(":/res/sg_logo_error.png"))
        self.logo_example.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.logo_example.setObjectName("logo_example")
        self.gridLayout.addWidget(self.logo_example, 1, 1, 3, 1)
        self.summary_lbl = QtGui.QLabel(ErrorWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        font.setWeight(50)
        font.setBold(False)
        self.summary_lbl.setFont(font)
        self.summary_lbl.setText("")
        self.summary_lbl.setObjectName("summary_lbl")
        self.gridLayout.addWidget(self.summary_lbl, 1, 2, 1, 2)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(ErrorWidget)
        QtCore.QMetaObject.connectSlotsByName(ErrorWidget)

    def retranslateUi(self, ErrorWidget):
        ErrorWidget.setWindowTitle(QtGui.QApplication.translate("ErrorWidget", "Quickdailies", None, QtGui.QApplication.UnicodeUTF8))
        self.close_btn.setText(QtGui.QApplication.translate("ErrorWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
