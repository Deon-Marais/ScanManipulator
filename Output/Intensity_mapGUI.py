# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Output\Intensity_mapGUI.ui'
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

class Ui_Intensity_map(object):
    def setupUi(self, Intensity_map):
        Intensity_map.setObjectName(_fromUtf8("Intensity_map"))
        Intensity_map.resize(330, 305)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Intensity_map.sizePolicy().hasHeightForWidth())
        Intensity_map.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Intensity_map)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.all_radio = QtGui.QRadioButton(Intensity_map)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.all_radio.sizePolicy().hasHeightForWidth())
        self.all_radio.setSizePolicy(sizePolicy)
        self.all_radio.setChecked(True)
        self.all_radio.setObjectName(_fromUtf8("all_radio"))
        self.horizontalLayout.addWidget(self.all_radio)
        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.current_radio = QtGui.QRadioButton(Intensity_map)
        self.current_radio.setObjectName(_fromUtf8("current_radio"))
        self.horizontalLayout.addWidget(self.current_radio)
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.range_radio = QtGui.QRadioButton(Intensity_map)
        self.range_radio.setObjectName(_fromUtf8("range_radio"))
        self.horizontalLayout.addWidget(self.range_radio)
        self.rangemin_spin = QtGui.QSpinBox(Intensity_map)
        self.rangemin_spin.setObjectName(_fromUtf8("rangemin_spin"))
        self.horizontalLayout.addWidget(self.rangemin_spin)
        self.label_2 = QtGui.QLabel(Intensity_map)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.rangemax_spin = QtGui.QSpinBox(Intensity_map)
        self.rangemax_spin.setObjectName(_fromUtf8("rangemax_spin"))
        self.horizontalLayout.addWidget(self.rangemax_spin)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.CreateButton = QtGui.QPushButton(Intensity_map)
        self.CreateButton.setObjectName(_fromUtf8("CreateButton"))
        self.gridLayout.addWidget(self.CreateButton, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(Intensity_map)
        QtCore.QObject.connect(self.CreateButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Intensity_map.CreateMap)
        QtCore.QMetaObject.connectSlotsByName(Intensity_map)

    def retranslateUi(self, Intensity_map):
        Intensity_map.setWindowTitle(_translate("Intensity_map", "Intenity Map", None))
        Intensity_map.setTitle(_translate("Intensity_map", "Ascii Export", None))
        self.all_radio.setText(_translate("Intensity_map", "All", None))
        self.current_radio.setText(_translate("Intensity_map", "Current", None))
        self.range_radio.setText(_translate("Intensity_map", "Range:", None))
        self.label_2.setText(_translate("Intensity_map", "to", None))
        self.CreateButton.setText(_translate("Intensity_map", "Create", None))

