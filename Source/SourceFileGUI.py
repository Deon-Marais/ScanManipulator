# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Source\SourceFileGUI.ui'
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

class Ui_SourceFile(object):
    def setupUi(self, SourceFile):
        SourceFile.setObjectName(_fromUtf8("SourceFile"))
        SourceFile.resize(296, 220)
        SourceFile.setMinimumSize(QtCore.QSize(0, 170))
        self.verticalLayout = QtGui.QVBoxLayout(SourceFile)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.filename_edit = QtGui.QLineEdit(SourceFile)
        self.filename_edit.setEnabled(True)
        self.filename_edit.setText(_fromUtf8(""))
        self.filename_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.filename_edit.setReadOnly(True)
        self.filename_edit.setObjectName(_fromUtf8("filename_edit"))
        self.horizontalLayout.addWidget(self.filename_edit)
        self.open_button = QtGui.QPushButton(SourceFile)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_button.sizePolicy().hasHeightForWidth())
        self.open_button.setSizePolicy(sizePolicy)
        self.open_button.setObjectName(_fromUtf8("open_button"))
        self.horizontalLayout.addWidget(self.open_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lim_mem_check = QtGui.QCheckBox(SourceFile)
        self.lim_mem_check.setObjectName(_fromUtf8("lim_mem_check"))
        self.verticalLayout.addWidget(self.lim_mem_check)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.file_tbl = QtGui.QTableWidget(SourceFile)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_tbl.sizePolicy().hasHeightForWidth())
        self.file_tbl.setSizePolicy(sizePolicy)
        self.file_tbl.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.file_tbl.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.file_tbl.setTextElideMode(QtCore.Qt.ElideLeft)
        self.file_tbl.setObjectName(_fromUtf8("file_tbl"))
        self.file_tbl.setColumnCount(4)
        self.file_tbl.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.file_tbl.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.file_tbl.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.file_tbl.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.file_tbl.setHorizontalHeaderItem(3, item)
        self.file_tbl.horizontalHeader().setDefaultSectionSize(80)
        self.file_tbl.horizontalHeader().setMinimumSectionSize(19)
        self.file_tbl.verticalHeader().setVisible(False)
        self.file_tbl.verticalHeader().setDefaultSectionSize(25)
        self.horizontalLayout_2.addWidget(self.file_tbl)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.remove_btn = QtGui.QPushButton(SourceFile)
        self.remove_btn.setObjectName(_fromUtf8("remove_btn"))
        self.verticalLayout_2.addWidget(self.remove_btn)
        self.select_btn = QtGui.QPushButton(SourceFile)
        self.select_btn.setObjectName(_fromUtf8("select_btn"))
        self.verticalLayout_2.addWidget(self.select_btn)
        self.unselect_btn = QtGui.QPushButton(SourceFile)
        self.unselect_btn.setObjectName(_fromUtf8("unselect_btn"))
        self.verticalLayout_2.addWidget(self.unselect_btn)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(SourceFile)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.nrfiles_label = QtGui.QLabel(SourceFile)
        self.nrfiles_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nrfiles_label.setObjectName(_fromUtf8("nrfiles_label"))
        self.horizontalLayout_3.addWidget(self.nrfiles_label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_3 = QtGui.QLabel(SourceFile)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.nrselected_label = QtGui.QLabel(SourceFile)
        self.nrselected_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nrselected_label.setObjectName(_fromUtf8("nrselected_label"))
        self.horizontalLayout_3.addWidget(self.nrselected_label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(SourceFile)
        QtCore.QObject.connect(self.open_button, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), SourceFile.OpenFile)
        QtCore.QObject.connect(self.remove_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), SourceFile.Remove)
        QtCore.QObject.connect(self.select_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), SourceFile.Select)
        QtCore.QObject.connect(self.unselect_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), SourceFile.Unselect)
        QtCore.QObject.connect(self.file_tbl, QtCore.SIGNAL(_fromUtf8("cellClicked(int,int)")), SourceFile.RowDoubleClicked)
        QtCore.QObject.connect(self.file_tbl, QtCore.SIGNAL(_fromUtf8("cellChanged(int,int)")), SourceFile.CellValueChanged)
        QtCore.QMetaObject.connectSlotsByName(SourceFile)

    def retranslateUi(self, SourceFile):
        SourceFile.setWindowTitle(_translate("SourceFile", "SourceFile", None))
        SourceFile.setTitle(_translate("SourceFile", "SourceFile", None))
        self.open_button.setText(_translate("SourceFile", "Open", None))
        self.lim_mem_check.setText(_translate("SourceFile", "Conserve mem usage", None))
        item = self.file_tbl.horizontalHeaderItem(0)
        item.setText(_translate("SourceFile", "Filename", None))
        item = self.file_tbl.horizontalHeaderItem(1)
        item.setText(_translate("SourceFile", "Ext", None))
        item = self.file_tbl.horizontalHeaderItem(2)
        item.setText(_translate("SourceFile", "Type", None))
        item = self.file_tbl.horizontalHeaderItem(3)
        item.setText(_translate("SourceFile", "Location", None))
        self.remove_btn.setText(_translate("SourceFile", "Remove", None))
        self.select_btn.setText(_translate("SourceFile", "Select", None))
        self.unselect_btn.setText(_translate("SourceFile", "Unselect", None))
        self.label.setText(_translate("SourceFile", "Total nr Files:", None))
        self.nrfiles_label.setText(_translate("SourceFile", "0", None))
        self.label_3.setText(_translate("SourceFile", "Files to export (selected):", None))
        self.nrselected_label.setText(_translate("SourceFile", "0", None))

