# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Manipulate\ManipulateGUI.ui'
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

class Ui_Manipulate(object):
    def setupUi(self, Manipulate):
        Manipulate.setObjectName(_fromUtf8("Manipulate"))
        Manipulate.setWindowModality(QtCore.Qt.ApplicationModal)
        Manipulate.resize(622, 247)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Manipulate)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.datasetappliedLayout = QtGui.QHBoxLayout()
        self.datasetappliedLayout.setSpacing(0)
        self.datasetappliedLayout.setObjectName(_fromUtf8("datasetappliedLayout"))
        self.datasetsappliedframe = QtGui.QFrame(Manipulate)
        self.datasetsappliedframe.setFrameShape(QtGui.QFrame.StyledPanel)
        self.datasetsappliedframe.setFrameShadow(QtGui.QFrame.Raised)
        self.datasetsappliedframe.setObjectName(_fromUtf8("datasetsappliedframe"))
        self.datasetappliedLayout.addWidget(self.datasetsappliedframe)
        self.verticalLayout.addLayout(self.datasetappliedLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Manipulate)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.vx_combo = QtGui.QComboBox(Manipulate)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vx_combo.sizePolicy().hasHeightForWidth())
        self.vx_combo.setSizePolicy(sizePolicy)
        self.vx_combo.setObjectName(_fromUtf8("vx_combo"))
        self.horizontalLayout.addWidget(self.vx_combo)
        self.label_2 = QtGui.QLabel(Manipulate)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.vy_combo = QtGui.QComboBox(Manipulate)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vy_combo.sizePolicy().hasHeightForWidth())
        self.vy_combo.setSizePolicy(sizePolicy)
        self.vy_combo.setObjectName(_fromUtf8("vy_combo"))
        self.horizontalLayout.addWidget(self.vy_combo)
        self.angle_edit = QtGui.QLineEdit(Manipulate)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.angle_edit.sizePolicy().hasHeightForWidth())
        self.angle_edit.setSizePolicy(sizePolicy)
        self.angle_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.angle_edit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.angle_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.angle_edit.setObjectName(_fromUtf8("angle_edit"))
        self.horizontalLayout.addWidget(self.angle_edit)
        self.label_3 = QtGui.QLabel(Manipulate)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.vaxesgo_btn = QtGui.QPushButton(Manipulate)
        self.vaxesgo_btn.setObjectName(_fromUtf8("vaxesgo_btn"))
        self.horizontalLayout.addWidget(self.vaxesgo_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_4 = QtGui.QLabel(Manipulate)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.ythreshold_edit = QtGui.QLineEdit(Manipulate)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ythreshold_edit.sizePolicy().hasHeightForWidth())
        self.ythreshold_edit.setSizePolicy(sizePolicy)
        self.ythreshold_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.ythreshold_edit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.ythreshold_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ythreshold_edit.setObjectName(_fromUtf8("ythreshold_edit"))
        self.horizontalLayout_2.addWidget(self.ythreshold_edit)
        self.label_5 = QtGui.QLabel(Manipulate)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.thresholddataset_edit = QtGui.QLineEdit(Manipulate)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thresholddataset_edit.sizePolicy().hasHeightForWidth())
        self.thresholddataset_edit.setSizePolicy(sizePolicy)
        self.thresholddataset_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.thresholddataset_edit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.thresholddataset_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.thresholddataset_edit.setObjectName(_fromUtf8("thresholddataset_edit"))
        self.horizontalLayout_2.addWidget(self.thresholddataset_edit)
        self.removebelowthresholdgo_btn = QtGui.QPushButton(Manipulate)
        self.removebelowthresholdgo_btn.setObjectName(_fromUtf8("removebelowthresholdgo_btn"))
        self.horizontalLayout_2.addWidget(self.removebelowthresholdgo_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_6 = QtGui.QLabel(Manipulate)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.removeevery_edit = QtGui.QLineEdit(Manipulate)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeevery_edit.sizePolicy().hasHeightForWidth())
        self.removeevery_edit.setSizePolicy(sizePolicy)
        self.removeevery_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.removeevery_edit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.removeevery_edit.setObjectName(_fromUtf8("removeevery_edit"))
        self.horizontalLayout_3.addWidget(self.removeevery_edit)
        self.label_7 = QtGui.QLabel(Manipulate)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_3.addWidget(self.label_7)
        self.removeeverygo_btn = QtGui.QPushButton(Manipulate)
        self.removeeverygo_btn.setObjectName(_fromUtf8("removeeverygo_btn"))
        self.horizontalLayout_3.addWidget(self.removeeverygo_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_8 = QtGui.QLabel(Manipulate)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_4.addWidget(self.label_8)
        self.horizontal_radio = QtGui.QRadioButton(Manipulate)
        self.horizontal_radio.setChecked(True)
        self.horizontal_radio.setObjectName(_fromUtf8("horizontal_radio"))
        self.horizontalLayout_4.addWidget(self.horizontal_radio)
        self.vertical_radio = QtGui.QRadioButton(Manipulate)
        self.vertical_radio.setObjectName(_fromUtf8("vertical_radio"))
        self.horizontalLayout_4.addWidget(self.vertical_radio)
        self.label_9 = QtGui.QLabel(Manipulate)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_4.addWidget(self.label_9)
        self.rebinx_edit = QtGui.QLineEdit(Manipulate)
        self.rebinx_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.rebinx_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.rebinx_edit.setObjectName(_fromUtf8("rebinx_edit"))
        self.horizontalLayout_4.addWidget(self.rebinx_edit)
        self.label_10 = QtGui.QLabel(Manipulate)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_4.addWidget(self.label_10)
        self.rebiny_edit = QtGui.QLineEdit(Manipulate)
        self.rebiny_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.rebiny_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.rebiny_edit.setObjectName(_fromUtf8("rebiny_edit"))
        self.horizontalLayout_4.addWidget(self.rebiny_edit)
        self.extractdetectorlines_btn = QtGui.QPushButton(Manipulate)
        self.extractdetectorlines_btn.setObjectName(_fromUtf8("extractdetectorlines_btn"))
        self.horizontalLayout_4.addWidget(self.extractdetectorlines_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.transposexy_check = QtGui.QCheckBox(Manipulate)
        self.transposexy_check.setObjectName(_fromUtf8("transposexy_check"))
        self.verticalLayout_2.addWidget(self.transposexy_check)
        self.transposego_btn = QtGui.QPushButton(Manipulate)
        self.transposego_btn.setEnabled(False)
        self.transposego_btn.setObjectName(_fromUtf8("transposego_btn"))
        self.verticalLayout_2.addWidget(self.transposego_btn)
        self.pushButton = QtGui.QPushButton(Manipulate)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_2.addWidget(self.pushButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(Manipulate)
        QtCore.QObject.connect(self.vaxesgo_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), Manipulate.AddVirtualAxes)
        QtCore.QObject.connect(self.removebelowthresholdgo_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), Manipulate.RemoveBelowThreshold)
        QtCore.QObject.connect(self.removeeverygo_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), Manipulate.RemoveEverynth)
        QtCore.QObject.connect(self.transposego_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), Manipulate.Transposexy)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Manipulate.Test)
        QtCore.QObject.connect(self.extractdetectorlines_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), Manipulate.ExtractDetectorLines)
        QtCore.QMetaObject.connectSlotsByName(Manipulate)

    def retranslateUi(self, Manipulate):
        Manipulate.setWindowTitle(_translate("Manipulate", "Manipulate parameters", None))
        self.label.setText(_translate("Manipulate", "Add virtual axes (vsx and vsy) by rotating ", None))
        self.label_2.setText(_translate("Manipulate", "and", None))
        self.angle_edit.setText(_translate("Manipulate", "45", None))
        self.label_3.setText(_translate("Manipulate", "degrees", None))
        self.vaxesgo_btn.setText(_translate("Manipulate", "Go", None))
        self.label_4.setText(_translate("Manipulate", "New datagroup: Remove datapoints where y is below below threshold of ", None))
        self.ythreshold_edit.setText(_translate("Manipulate", "200", None))
        self.label_5.setText(_translate("Manipulate", "in dataset ", None))
        self.thresholddataset_edit.setText(_translate("Manipulate", "0", None))
        self.removebelowthresholdgo_btn.setText(_translate("Manipulate", "Go", None))
        self.label_6.setText(_translate("Manipulate", "New datagroup: Remove every ", None))
        self.removeevery_edit.setText(_translate("Manipulate", "3", None))
        self.label_7.setText(_translate("Manipulate", " dataset ", None))
        self.removeeverygo_btn.setText(_translate("Manipulate", "Go", None))
        self.label_8.setText(_translate("Manipulate", "Datasets from detector lines", None))
        self.horizontal_radio.setText(_translate("Manipulate", "Horizontal", None))
        self.vertical_radio.setText(_translate("Manipulate", "Vertical", None))
        self.label_9.setText(_translate("Manipulate", "Rebin x:", None))
        self.rebinx_edit.setText(_translate("Manipulate", "-1", None))
        self.label_10.setText(_translate("Manipulate", "Rebin y:", None))
        self.rebiny_edit.setText(_translate("Manipulate", "25", None))
        self.extractdetectorlines_btn.setText(_translate("Manipulate", "Go", None))
        self.transposexy_check.setText(_translate("Manipulate", "Transpose xy", None))
        self.transposego_btn.setText(_translate("Manipulate", "Transpose xy", None))
        self.pushButton.setText(_translate("Manipulate", "Test", None))

