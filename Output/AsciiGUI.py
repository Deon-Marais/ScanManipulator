# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Output\AsciiGUI.ui'
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

class Ui_Ascii(object):
    def setupUi(self, Ascii):
        Ascii.setObjectName(_fromUtf8("Ascii"))
        Ascii.resize(383, 305)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Ascii.sizePolicy().hasHeightForWidth())
        Ascii.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Ascii)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(Ascii)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.files_all_radio = QtGui.QRadioButton(Ascii)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.files_all_radio.sizePolicy().hasHeightForWidth())
        self.files_all_radio.setSizePolicy(sizePolicy)
        self.files_all_radio.setChecked(True)
        self.files_all_radio.setAutoExclusive(True)
        self.files_all_radio.setObjectName(_fromUtf8("files_all_radio"))
        self.buttonGroup = QtGui.QButtonGroup(Ascii)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.files_all_radio)
        self.horizontalLayout_2.addWidget(self.files_all_radio)
        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.files_current_radio = QtGui.QRadioButton(Ascii)
        self.files_current_radio.setObjectName(_fromUtf8("files_current_radio"))
        self.buttonGroup.addButton(self.files_current_radio)
        self.horizontalLayout_2.addWidget(self.files_current_radio)
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.files_range_radio = QtGui.QRadioButton(Ascii)
        self.files_range_radio.setEnabled(False)
        self.files_range_radio.setObjectName(_fromUtf8("files_range_radio"))
        self.buttonGroup.addButton(self.files_range_radio)
        self.horizontalLayout_2.addWidget(self.files_range_radio)
        self.files_rangemin_spin = QtGui.QSpinBox(Ascii)
        self.files_rangemin_spin.setEnabled(False)
        self.files_rangemin_spin.setObjectName(_fromUtf8("files_rangemin_spin"))
        self.horizontalLayout_2.addWidget(self.files_rangemin_spin)
        self.label_4 = QtGui.QLabel(Ascii)
        self.label_4.setEnabled(False)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.files_rangemax_spin = QtGui.QSpinBox(Ascii)
        self.files_rangemax_spin.setEnabled(False)
        self.files_rangemax_spin.setObjectName(_fromUtf8("files_rangemax_spin"))
        self.horizontalLayout_2.addWidget(self.files_rangemax_spin)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.combine_files_check = QtGui.QCheckBox(Ascii)
        self.combine_files_check.setChecked(True)
        self.combine_files_check.setObjectName(_fromUtf8("combine_files_check"))
        self.verticalLayout.addWidget(self.combine_files_check)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Ascii)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.dset_all_radio = QtGui.QRadioButton(Ascii)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dset_all_radio.sizePolicy().hasHeightForWidth())
        self.dset_all_radio.setSizePolicy(sizePolicy)
        self.dset_all_radio.setChecked(True)
        self.dset_all_radio.setObjectName(_fromUtf8("dset_all_radio"))
        self.horizontalLayout.addWidget(self.dset_all_radio)
        spacerItem2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.dset_current_radio = QtGui.QRadioButton(Ascii)
        self.dset_current_radio.setObjectName(_fromUtf8("dset_current_radio"))
        self.horizontalLayout.addWidget(self.dset_current_radio)
        spacerItem3 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.dset_range_radio = QtGui.QRadioButton(Ascii)
        self.dset_range_radio.setObjectName(_fromUtf8("dset_range_radio"))
        self.horizontalLayout.addWidget(self.dset_range_radio)
        self.dset_rangemin_spin = QtGui.QSpinBox(Ascii)
        self.dset_rangemin_spin.setObjectName(_fromUtf8("dset_rangemin_spin"))
        self.horizontalLayout.addWidget(self.dset_rangemin_spin)
        self.label_2 = QtGui.QLabel(Ascii)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.dset_rangemax_spin = QtGui.QSpinBox(Ascii)
        self.dset_rangemax_spin.setObjectName(_fromUtf8("dset_rangemax_spin"))
        self.horizontalLayout.addWidget(self.dset_rangemax_spin)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.FullProfButton = QtGui.QPushButton(Ascii)
        self.FullProfButton.setObjectName(_fromUtf8("FullProfButton"))
        self.gridLayout.addWidget(self.FullProfButton, 0, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.GSASButton = QtGui.QPushButton(Ascii)
        self.GSASButton.setObjectName(_fromUtf8("GSASButton"))
        self.horizontalLayout_3.addWidget(self.GSASButton)
        self.GSASLinkProfileCheckBox = QtGui.QCheckBox(Ascii)
        self.GSASLinkProfileCheckBox.setObjectName(_fromUtf8("GSASLinkProfileCheckBox"))
        self.horizontalLayout_3.addWidget(self.GSASLinkProfileCheckBox)
        self.GSASProfileLineEdit = QtGui.QLineEdit(Ascii)
        self.GSASProfileLineEdit.setObjectName(_fromUtf8("GSASProfileLineEdit"))
        self.horizontalLayout_3.addWidget(self.GSASProfileLineEdit)
        self.pushButton = QtGui.QPushButton(Ascii)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(20, 16777215))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)

        self.retranslateUi(Ascii)
        QtCore.QObject.connect(self.GSASButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Ascii.ExportGSAS)
        QtCore.QObject.connect(self.FullProfButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Ascii.ExportFullprof)
        QtCore.QObject.connect(self.combine_files_check, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), Ascii.CombinedChanged)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Ascii.OpenFileGSASProfile)
        QtCore.QMetaObject.connectSlotsByName(Ascii)

    def retranslateUi(self, Ascii):
        Ascii.setWindowTitle(_translate("Ascii", "Ascii", None))
        Ascii.setTitle(_translate("Ascii", "Ascii Export", None))
        self.label_3.setText(_translate("Ascii", "Files:       ", None))
        self.files_all_radio.setText(_translate("Ascii", "All", None))
        self.files_current_radio.setText(_translate("Ascii", "Current", None))
        self.files_range_radio.setText(_translate("Ascii", "Range:", None))
        self.label_4.setText(_translate("Ascii", "to", None))
        self.combine_files_check.setText(_translate("Ascii", "Combine Files", None))
        self.label.setText(_translate("Ascii", "Datasets:", None))
        self.dset_all_radio.setText(_translate("Ascii", "All", None))
        self.dset_current_radio.setText(_translate("Ascii", "Current", None))
        self.dset_range_radio.setText(_translate("Ascii", "Range:", None))
        self.label_2.setText(_translate("Ascii", "to", None))
        self.FullProfButton.setText(_translate("Ascii", "FullProf (*.xy)", None))
        self.GSASButton.setText(_translate("Ascii", "GSAS (*.zip)", None))
        self.GSASLinkProfileCheckBox.setText(_translate("Ascii", "Link profile", None))
        self.pushButton.setText(_translate("Ascii", "...", None))
