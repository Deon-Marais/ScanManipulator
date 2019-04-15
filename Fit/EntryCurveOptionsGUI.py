# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fit\EntryCurveOptionsGUI.ui'
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

class Ui_EntryCurveOptions(object):
    def setupUi(self, EntryCurveOptions):
        EntryCurveOptions.setObjectName(_fromUtf8("EntryCurveOptions"))
        EntryCurveOptions.resize(376, 85)
        EntryCurveOptions.setMinimumSize(QtCore.QSize(0, 50))
        EntryCurveOptions.setTitle(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(EntryCurveOptions)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.transmission_radio = QtGui.QRadioButton(EntryCurveOptions)
        self.transmission_radio.setObjectName(_fromUtf8("transmission_radio"))
        self.gridLayout.addWidget(self.transmission_radio, 0, 1, 1, 1)
        self.reflection_radio = QtGui.QRadioButton(EntryCurveOptions)
        self.reflection_radio.setChecked(True)
        self.reflection_radio.setObjectName(_fromUtf8("reflection_radio"))
        self.gridLayout.addWidget(self.reflection_radio, 0, 0, 1, 1)
        self.zscan_radio = QtGui.QRadioButton(EntryCurveOptions)
        self.zscan_radio.setObjectName(_fromUtf8("zscan_radio"))
        self.gridLayout.addWidget(self.zscan_radio, 0, 2, 1, 1)
        self.wall_check = QtGui.QCheckBox(EntryCurveOptions)
        self.wall_check.setObjectName(_fromUtf8("wall_check"))
        self.gridLayout.addWidget(self.wall_check, 0, 3, 1, 1)

        self.retranslateUi(EntryCurveOptions)
        QtCore.QObject.connect(self.reflection_radio, QtCore.SIGNAL(_fromUtf8("clicked()")), EntryCurveOptions.typeChanged)
        QtCore.QObject.connect(self.transmission_radio, QtCore.SIGNAL(_fromUtf8("clicked()")), EntryCurveOptions.typeChanged)
        QtCore.QObject.connect(self.zscan_radio, QtCore.SIGNAL(_fromUtf8("clicked()")), EntryCurveOptions.typeChanged)
        QtCore.QObject.connect(self.wall_check, QtCore.SIGNAL(_fromUtf8("clicked()")), EntryCurveOptions.typeChanged)
        QtCore.QMetaObject.connectSlotsByName(EntryCurveOptions)

    def retranslateUi(self, EntryCurveOptions):
        EntryCurveOptions.setWindowTitle(_translate("EntryCurveOptions", "EntryCurve", None))
        self.transmission_radio.setText(_translate("EntryCurveOptions", "Transmission", None))
        self.reflection_radio.setText(_translate("EntryCurveOptions", "Reflection", None))
        self.zscan_radio.setText(_translate("EntryCurveOptions", "Z-scan", None))
        self.wall_check.setText(_translate("EntryCurveOptions", "Wall", None))

