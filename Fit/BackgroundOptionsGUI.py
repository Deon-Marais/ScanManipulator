# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fit\BackgroundOptionsGUI.ui'
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

class Ui_BackgroundOptions(object):
    def setupUi(self, BackgroundOptions):
        BackgroundOptions.setObjectName(_fromUtf8("BackgroundOptions"))
        BackgroundOptions.resize(345, 79)
        BackgroundOptions.setCheckable(True)
        BackgroundOptions.setChecked(False)
        self.gridLayout = QtGui.QGridLayout(BackgroundOptions)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.bgnonpeaks_radio = QtGui.QRadioButton(BackgroundOptions)
        self.bgnonpeaks_radio.setChecked(True)
        self.bgnonpeaks_radio.setObjectName(_fromUtf8("bgnonpeaks_radio"))
        self.gridLayout.addWidget(self.bgnonpeaks_radio, 0, 0, 1, 1)
        self.bgrange_radio = QtGui.QRadioButton(BackgroundOptions)
        self.bgrange_radio.setObjectName(_fromUtf8("bgrange_radio"))
        self.gridLayout.addWidget(self.bgrange_radio, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(BackgroundOptions)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.bgstart_edit = QtGui.QLineEdit(BackgroundOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bgstart_edit.sizePolicy().hasHeightForWidth())
        self.bgstart_edit.setSizePolicy(sizePolicy)
        self.bgstart_edit.setMinimumSize(QtCore.QSize(10, 0))
        self.bgstart_edit.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.bgstart_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bgstart_edit.setObjectName(_fromUtf8("bgstart_edit"))
        self.gridLayout.addWidget(self.bgstart_edit, 0, 3, 1, 1)
        self.label_5 = QtGui.QLabel(BackgroundOptions)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 4, 1, 1)
        self.bgend_edit = QtGui.QLineEdit(BackgroundOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bgend_edit.sizePolicy().hasHeightForWidth())
        self.bgend_edit.setSizePolicy(sizePolicy)
        self.bgend_edit.setMinimumSize(QtCore.QSize(10, 0))
        self.bgend_edit.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.bgend_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bgend_edit.setObjectName(_fromUtf8("bgend_edit"))
        self.gridLayout.addWidget(self.bgend_edit, 0, 5, 1, 1)
        self.bgsinglefixed_radio = QtGui.QRadioButton(BackgroundOptions)
        self.bgsinglefixed_radio.setChecked(False)
        self.bgsinglefixed_radio.setObjectName(_fromUtf8("bgsinglefixed_radio"))
        self.gridLayout.addWidget(self.bgsinglefixed_radio, 1, 0, 1, 1)
        self.bgallfixed_radio = QtGui.QRadioButton(BackgroundOptions)
        self.bgallfixed_radio.setObjectName(_fromUtf8("bgallfixed_radio"))
        self.gridLayout.addWidget(self.bgallfixed_radio, 1, 1, 1, 1)
        self.bgfix_edit = QtGui.QLineEdit(BackgroundOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bgfix_edit.sizePolicy().hasHeightForWidth())
        self.bgfix_edit.setSizePolicy(sizePolicy)
        self.bgfix_edit.setMinimumSize(QtCore.QSize(10, 0))
        self.bgfix_edit.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.bgfix_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bgfix_edit.setObjectName(_fromUtf8("bgfix_edit"))
        self.gridLayout.addWidget(self.bgfix_edit, 1, 2, 1, 1)

        self.retranslateUi(BackgroundOptions)
        QtCore.QMetaObject.connectSlotsByName(BackgroundOptions)

    def retranslateUi(self, BackgroundOptions):
        BackgroundOptions.setWindowTitle(_translate("BackgroundOptions", "BackgroundOptions", None))
        BackgroundOptions.setTitle(_translate("BackgroundOptions", "Background", None))
        self.bgnonpeaks_radio.setText(_translate("BackgroundOptions", "Non-peaks", None))
        self.bgrange_radio.setText(_translate("BackgroundOptions", "Fixed range -->", None))
        self.label_4.setText(_translate("BackgroundOptions", "bg_start:", None))
        self.bgstart_edit.setText(_translate("BackgroundOptions", "0", None))
        self.label_5.setText(_translate("BackgroundOptions", "bg_end:", None))
        self.bgend_edit.setText(_translate("BackgroundOptions", "0", None))
        self.bgsinglefixed_radio.setText(_translate("BackgroundOptions", "Single fixed", None))
        self.bgallfixed_radio.setText(_translate("BackgroundOptions", "All fixed:", None))
        self.bgfix_edit.setText(_translate("BackgroundOptions", "0", None))

