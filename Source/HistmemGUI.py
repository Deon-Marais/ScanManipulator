# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Source\HistmemGUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Histmem(object):
    def setupUi(self, Histmem):
        Histmem.setObjectName(_fromUtf8("Histmem"))
        Histmem.resize(318, 141)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Histmem.sizePolicy().hasHeightForWidth())
        Histmem.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Histmem)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(Histmem)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.servername_edit = QtGui.QLineEdit(Histmem)
        self.servername_edit.setEnabled(True)
        self.servername_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.servername_edit.setReadOnly(False)
        self.servername_edit.setObjectName(_fromUtf8("servername_edit"))
        self.horizontalLayout_3.addWidget(self.servername_edit)
        self.read_button = QtGui.QPushButton(Histmem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.read_button.sizePolicy().hasHeightForWidth())
        self.read_button.setSizePolicy(sizePolicy)
        self.read_button.setObjectName(_fromUtf8("read_button"))
        self.horizontalLayout_3.addWidget(self.read_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.autoread_check = QtGui.QCheckBox(Histmem)
        self.autoread_check.setChecked(False)
        self.autoread_check.setObjectName(_fromUtf8("autoread_check"))
        self.horizontalLayout_2.addWidget(self.autoread_check)
        self.autoreadtime_edit = QtGui.QLineEdit(Histmem)
        self.autoreadtime_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.autoreadtime_edit.setObjectName(_fromUtf8("autoreadtime_edit"))
        self.horizontalLayout_2.addWidget(self.autoreadtime_edit)
        self.label_2 = QtGui.QLabel(Histmem)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Histmem)
        QtCore.QObject.connect(self.read_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Histmem.ReadServer)
        QtCore.QObject.connect(self.autoread_check, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), Histmem.ARSelected)
        QtCore.QObject.connect(self.servername_edit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), Histmem.ServerChanged)
        QtCore.QMetaObject.connectSlotsByName(Histmem)

    def retranslateUi(self, Histmem):
        Histmem.setWindowTitle(_translate("Histmem", "Histmem", None))
        Histmem.setTitle(_translate("Histmem", "ANSTO Histogram Memory", None))
        self.label.setText(_translate("Histmem", "Server", None))
        self.servername_edit.setText(_translate("Histmem", "http://10.0.1.21", None))
        self.read_button.setText(_translate("Histmem", "Read", None))
        self.autoread_check.setText(_translate("Histmem", "Autoread every", None))
        self.autoreadtime_edit.setText(_translate("Histmem", "2", None))
        self.label_2.setText(_translate("Histmem", "seconds", None))

