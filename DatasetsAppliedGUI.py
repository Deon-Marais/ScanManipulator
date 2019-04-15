# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatasetsAppliedGUI.ui'
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

class Ui_DatasetsApplied(object):
    def setupUi(self, DatasetsApplied):
        DatasetsApplied.setObjectName(_fromUtf8("DatasetsApplied"))
        DatasetsApplied.resize(521, 42)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DatasetsApplied.sizePolicy().hasHeightForWidth())
        DatasetsApplied.setSizePolicy(sizePolicy)
        DatasetsApplied.setFrameShape(QtGui.QFrame.StyledPanel)
        DatasetsApplied.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(DatasetsApplied)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.allfiles_check = QtGui.QCheckBox(DatasetsApplied)
        self.allfiles_check.setObjectName(_fromUtf8("allfiles_check"))
        self.horizontalLayout.addWidget(self.allfiles_check)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(DatasetsApplied)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.all_radio = QtGui.QRadioButton(DatasetsApplied)
        self.all_radio.setChecked(True)
        self.all_radio.setObjectName(_fromUtf8("all_radio"))
        self.horizontalLayout.addWidget(self.all_radio)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.current_radio = QtGui.QRadioButton(DatasetsApplied)
        self.current_radio.setObjectName(_fromUtf8("current_radio"))
        self.horizontalLayout.addWidget(self.current_radio)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.range_radio = QtGui.QRadioButton(DatasetsApplied)
        self.range_radio.setObjectName(_fromUtf8("range_radio"))
        self.horizontalLayout.addWidget(self.range_radio)
        self.rangemin_spin = QtGui.QSpinBox(DatasetsApplied)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangemin_spin.sizePolicy().hasHeightForWidth())
        self.rangemin_spin.setSizePolicy(sizePolicy)
        self.rangemin_spin.setMinimum(1)
        self.rangemin_spin.setMaximum(99999)
        self.rangemin_spin.setObjectName(_fromUtf8("rangemin_spin"))
        self.horizontalLayout.addWidget(self.rangemin_spin)
        self.label = QtGui.QLabel(DatasetsApplied)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.rangemax_spin = QtGui.QSpinBox(DatasetsApplied)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangemax_spin.sizePolicy().hasHeightForWidth())
        self.rangemax_spin.setSizePolicy(sizePolicy)
        self.rangemax_spin.setMinimum(1)
        self.rangemax_spin.setMaximum(99999)
        self.rangemax_spin.setObjectName(_fromUtf8("rangemax_spin"))
        self.horizontalLayout.addWidget(self.rangemax_spin)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DatasetsApplied)
        QtCore.QMetaObject.connectSlotsByName(DatasetsApplied)

    def retranslateUi(self, DatasetsApplied):
        DatasetsApplied.setWindowTitle(_translate("DatasetsApplied", "Frame", None))
        self.allfiles_check.setText(_translate("DatasetsApplied", "All Files", None))
        self.label_2.setText(_translate("DatasetsApplied", "Datasets:", None))
        self.all_radio.setText(_translate("DatasetsApplied", "All", None))
        self.current_radio.setText(_translate("DatasetsApplied", "Current", None))
        self.range_radio.setText(_translate("DatasetsApplied", "Range", None))
        self.label.setText(_translate("DatasetsApplied", "to", None))

