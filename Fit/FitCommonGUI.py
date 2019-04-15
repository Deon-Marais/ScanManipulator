# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fit\FitCommonGUI.ui'
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

class Ui_FitCommon(object):
    def setupUi(self, FitCommon):
        FitCommon.setObjectName(_fromUtf8("FitCommon"))
        FitCommon.resize(400, 430)
        FitCommon.setTitle(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(FitCommon)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.range_tbl = QtGui.QTableWidget(FitCommon)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.range_tbl.sizePolicy().hasHeightForWidth())
        self.range_tbl.setSizePolicy(sizePolicy)
        self.range_tbl.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.range_tbl.setObjectName(_fromUtf8("range_tbl"))
        self.range_tbl.setColumnCount(0)
        self.range_tbl.setRowCount(0)
        self.range_tbl.horizontalHeader().setDefaultSectionSize(80)
        self.range_tbl.horizontalHeader().setMinimumSectionSize(19)
        self.range_tbl.verticalHeader().setDefaultSectionSize(25)
        self.horizontalLayout_2.addWidget(self.range_tbl)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.addrange_btn = QtGui.QPushButton(FitCommon)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addrange_btn.sizePolicy().hasHeightForWidth())
        self.addrange_btn.setSizePolicy(sizePolicy)
        self.addrange_btn.setObjectName(_fromUtf8("addrange_btn"))
        self.verticalLayout_2.addWidget(self.addrange_btn)
        self.delrange_btn = QtGui.QPushButton(FitCommon)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delrange_btn.sizePolicy().hasHeightForWidth())
        self.delrange_btn.setSizePolicy(sizePolicy)
        self.delrange_btn.setObjectName(_fromUtf8("delrange_btn"))
        self.verticalLayout_2.addWidget(self.delrange_btn)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.moreOptionsLayout = QtGui.QVBoxLayout()
        self.moreOptionsLayout.setContentsMargins(-1, 0, -1, -1)
        self.moreOptionsLayout.setObjectName(_fromUtf8("moreOptionsLayout"))
        self.moreOptionsGroupBox = QtGui.QGroupBox(FitCommon)
        self.moreOptionsGroupBox.setMinimumSize(QtCore.QSize(0, 100))
        self.moreOptionsGroupBox.setObjectName(_fromUtf8("moreOptionsGroupBox"))
        self.moreOptionsLayout.addWidget(self.moreOptionsGroupBox)
        self.verticalLayout.addLayout(self.moreOptionsLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.varname_label = QtGui.QLabel(FitCommon)
        self.varname_label.setObjectName(_fromUtf8("varname_label"))
        self.horizontalLayout.addWidget(self.varname_label)
        self.var_slider = QtGui.QSlider(FitCommon)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.var_slider.sizePolicy().hasHeightForWidth())
        self.var_slider.setSizePolicy(sizePolicy)
        self.var_slider.setOrientation(QtCore.Qt.Horizontal)
        self.var_slider.setObjectName(_fromUtf8("var_slider"))
        self.horizontalLayout.addWidget(self.var_slider)
        self.varval_label = QtGui.QLabel(FitCommon)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.varval_label.sizePolicy().hasHeightForWidth())
        self.varval_label.setSizePolicy(sizePolicy)
        self.varval_label.setMinimumSize(QtCore.QSize(20, 0))
        self.varval_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.varval_label.setObjectName(_fromUtf8("varval_label"))
        self.horizontalLayout.addWidget(self.varval_label)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(FitCommon)
        QtCore.QObject.connect(self.range_tbl, QtCore.SIGNAL(_fromUtf8("itemSelectionChanged()")), FitCommon.UpdateUIValues)
        QtCore.QObject.connect(self.addrange_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), FitCommon.AddRange)
        QtCore.QObject.connect(self.delrange_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), FitCommon.DelRange)
        QtCore.QObject.connect(self.var_slider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), FitCommon.VarSliderValChanged)
        QtCore.QObject.connect(self.range_tbl, QtCore.SIGNAL(_fromUtf8("cellChanged(int,int)")), FitCommon.CellValueChanged)
        QtCore.QObject.connect(self.var_slider, QtCore.SIGNAL(_fromUtf8("sliderReleased()")), FitCommon.VarSliderReleased)
        QtCore.QMetaObject.connectSlotsByName(FitCommon)

    def retranslateUi(self, FitCommon):
        FitCommon.setWindowTitle(_translate("FitCommon", "FitCommon", None))
        self.addrange_btn.setText(_translate("FitCommon", "Add", None))
        self.delrange_btn.setText(_translate("FitCommon", "Del", None))
        self.moreOptionsGroupBox.setTitle(_translate("FitCommon", "MoreOptions", None))
        self.varname_label.setText(_translate("FitCommon", "FitVarName", None))
        self.varval_label.setText(_translate("FitCommon", "0", None))

