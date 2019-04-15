# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Output\SicsGUI.ui'
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

class Ui_Sics(object):
    def setupUi(self, Sics):
        Sics.setObjectName(_fromUtf8("Sics"))
        Sics.resize(358, 439)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Sics.sizePolicy().hasHeightForWidth())
        Sics.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Sics)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(Sics)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.port_Edit = QtGui.QLineEdit(Sics)
        self.port_Edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.port_Edit.setObjectName(_fromUtf8("port_Edit"))
        self.horizontalLayout_2.addWidget(self.port_Edit)
        self.label_4 = QtGui.QLabel(Sics)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.status_Edit = QtGui.QLabel(Sics)
        self.status_Edit.setObjectName(_fromUtf8("status_Edit"))
        self.horizontalLayout_2.addWidget(self.status_Edit)
        self.startserver_Button = QtGui.QPushButton(Sics)
        self.startserver_Button.setObjectName(_fromUtf8("startserver_Button"))
        self.horizontalLayout_2.addWidget(self.startserver_Button)
        self.stopserver_Button = QtGui.QPushButton(Sics)
        self.stopserver_Button.setObjectName(_fromUtf8("stopserver_Button"))
        self.horizontalLayout_2.addWidget(self.stopserver_Button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_2 = QtGui.QPushButton(Sics)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.label_2 = QtGui.QLabel(Sics)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.worstprm_label = QtGui.QLabel(Sics)
        self.worstprm_label.setObjectName(_fromUtf8("worstprm_label"))
        self.horizontalLayout.addWidget(self.worstprm_label)
        self.worstval_edit = QtGui.QLineEdit(Sics)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.worstval_edit.sizePolicy().hasHeightForWidth())
        self.worstval_edit.setSizePolicy(sizePolicy)
        self.worstval_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.worstval_edit.setReadOnly(True)
        self.worstval_edit.setObjectName(_fromUtf8("worstval_edit"))
        self.horizontalLayout.addWidget(self.worstval_edit)
        self.label_3 = QtGui.QLabel(Sics)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.compare_tbl = QtGui.QTableWidget(Sics)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.compare_tbl.sizePolicy().hasHeightForWidth())
        self.compare_tbl.setSizePolicy(sizePolicy)
        self.compare_tbl.setMinimumSize(QtCore.QSize(0, 180))
        self.compare_tbl.setObjectName(_fromUtf8("compare_tbl"))
        self.compare_tbl.setColumnCount(2)
        self.compare_tbl.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.compare_tbl.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.compare_tbl.setHorizontalHeaderItem(1, item)
        self.compare_tbl.horizontalHeader().setDefaultSectionSize(80)
        self.compare_tbl.horizontalHeader().setMinimumSectionSize(19)
        self.compare_tbl.verticalHeader().setDefaultSectionSize(25)
        self.verticalLayout.addWidget(self.compare_tbl)
        self.inbuffer_Edit = QtGui.QTextEdit(Sics)
        self.inbuffer_Edit.setObjectName(_fromUtf8("inbuffer_Edit"))
        self.verticalLayout.addWidget(self.inbuffer_Edit)

        self.retranslateUi(Sics)
        QtCore.QObject.connect(self.startserver_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), Sics.StartServer)
        QtCore.QObject.connect(self.stopserver_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), Sics.StopServer)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), Sics.GetCurrent)
        QtCore.QMetaObject.connectSlotsByName(Sics)

    def retranslateUi(self, Sics):
        Sics.setWindowTitle(_translate("Sics", "Sics", None))
        Sics.setTitle(_translate("Sics", "SICS Monitor Server", None))
        self.label.setText(_translate("Sics", "Port", None))
        self.port_Edit.setText(_translate("Sics", "30003", None))
        self.label_4.setText(_translate("Sics", "Status:", None))
        self.status_Edit.setText(_translate("Sics", "Off", None))
        self.startserver_Button.setText(_translate("Sics", "Start", None))
        self.stopserver_Button.setText(_translate("Sics", "Stop", None))
        self.pushButton_2.setText(_translate("Sics", "Get Current", None))
        self.label_2.setText(_translate("Sics", "Limiting parameter:", None))
        self.worstprm_label.setText(_translate("Sics", "--------------", None))
        self.label_3.setText(_translate("Sics", "%", None))
        item = self.compare_tbl.horizontalHeaderItem(0)
        item.setText(_translate("Sics", "Required", None))
        item = self.compare_tbl.horizontalHeaderItem(1)
        item.setText(_translate("Sics", "Current", None))

