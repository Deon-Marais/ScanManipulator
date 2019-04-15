# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fit\PeakProfilesOptionsGUI.ui'
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

class Ui_PeakProfilesOptions(object):
    def setupUi(self, PeakProfilesOptions):
        PeakProfilesOptions.setObjectName(_fromUtf8("PeakProfilesOptions"))
        PeakProfilesOptions.resize(376, 85)
        PeakProfilesOptions.setMinimumSize(QtCore.QSize(0, 50))
        PeakProfilesOptions.setTitle(_fromUtf8(""))
        self.horizontalLayout = QtGui.QHBoxLayout(PeakProfilesOptions)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.profileComboBox = QtGui.QComboBox(PeakProfilesOptions)
        self.profileComboBox.setObjectName(_fromUtf8("profileComboBox"))
        self.profileComboBox.addItem(_fromUtf8(""))
        self.profileComboBox.addItem(_fromUtf8(""))
        self.profileComboBox.addItem(_fromUtf8(""))
        self.profileComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.profileComboBox)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setMargin(10)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.reflection_radio = QtGui.QRadioButton(PeakProfilesOptions)
        self.reflection_radio.setChecked(True)
        self.reflection_radio.setObjectName(_fromUtf8("reflection_radio"))
        self.gridLayout.addWidget(self.reflection_radio, 0, 0, 1, 1)
        self.transmission_radio = QtGui.QRadioButton(PeakProfilesOptions)
        self.transmission_radio.setObjectName(_fromUtf8("transmission_radio"))
        self.gridLayout.addWidget(self.transmission_radio, 0, 1, 1, 1)
        self.zscan_radio = QtGui.QRadioButton(PeakProfilesOptions)
        self.zscan_radio.setObjectName(_fromUtf8("zscan_radio"))
        self.gridLayout.addWidget(self.zscan_radio, 1, 0, 1, 1)
        self.wall_radio = QtGui.QRadioButton(PeakProfilesOptions)
        self.wall_radio.setObjectName(_fromUtf8("wall_radio"))
        self.gridLayout.addWidget(self.wall_radio, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.backgroundLayout = QtGui.QHBoxLayout()
        self.backgroundLayout.setContentsMargins(-1, -1, 10, -1)
        self.backgroundLayout.setObjectName(_fromUtf8("backgroundLayout"))
        self.backgroundGroupBox = QtGui.QGroupBox(PeakProfilesOptions)
        self.backgroundGroupBox.setCheckable(False)
        self.backgroundGroupBox.setObjectName(_fromUtf8("backgroundGroupBox"))
        self.backgroundLayout.addWidget(self.backgroundGroupBox)
        self.horizontalLayout.addLayout(self.backgroundLayout)

        self.retranslateUi(PeakProfilesOptions)
        QtCore.QObject.connect(self.profileComboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), PeakProfilesOptions.typeChanged)
        QtCore.QMetaObject.connectSlotsByName(PeakProfilesOptions)

    def retranslateUi(self, PeakProfilesOptions):
        PeakProfilesOptions.setWindowTitle(_translate("PeakProfilesOptions", "PeakProfilesOptions", None))
        self.profileComboBox.setItemText(0, _translate("PeakProfilesOptions", "Gauss", None))
        self.profileComboBox.setItemText(1, _translate("PeakProfilesOptions", "Lorentz", None))
        self.profileComboBox.setItemText(2, _translate("PeakProfilesOptions", "Pseudo-Voigt", None))
        self.profileComboBox.setItemText(3, _translate("PeakProfilesOptions", "Pearson-VII", None))
        self.reflection_radio.setText(_translate("PeakProfilesOptions", "Reflection", None))
        self.transmission_radio.setText(_translate("PeakProfilesOptions", "Transmission", None))
        self.zscan_radio.setText(_translate("PeakProfilesOptions", "Z-scan", None))
        self.wall_radio.setText(_translate("PeakProfilesOptions", "Wall", None))
        self.backgroundGroupBox.setTitle(_translate("PeakProfilesOptions", "backgroundGroupBox", None))

