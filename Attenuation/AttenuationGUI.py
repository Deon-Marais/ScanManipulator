# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Attenuation\AttenuationGUI.ui'
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

class Ui_Attenuation(object):
    def setupUi(self, Attenuation):
        Attenuation.setObjectName(_fromUtf8("Attenuation"))
        Attenuation.setEnabled(True)
        Attenuation.resize(875, 637)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Attenuation.sizePolicy().hasHeightForWidth())
        Attenuation.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Attenuation)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.saveButton = QtGui.QPushButton(Attenuation)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout.addWidget(self.saveButton)
        self.loadButton = QtGui.QPushButton(Attenuation)
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.horizontalLayout.addWidget(self.loadButton)
        self.refresh_button = QtGui.QPushButton(Attenuation)
        self.refresh_button.setObjectName(_fromUtf8("refresh_button"))
        self.horizontalLayout.addWidget(self.refresh_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.animate_button = QtGui.QPushButton(Attenuation)
        self.animate_button.setObjectName(_fromUtf8("animate_button"))
        self.horizontalLayout_8.addWidget(self.animate_button)
        self.allfiles_check = QtGui.QCheckBox(Attenuation)
        self.allfiles_check.setObjectName(_fromUtf8("allfiles_check"))
        self.horizontalLayout_8.addWidget(self.allfiles_check)
        self.label_4 = QtGui.QLabel(Attenuation)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_8.addWidget(self.label_4)
        self.all_radio = QtGui.QRadioButton(Attenuation)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.all_radio.sizePolicy().hasHeightForWidth())
        self.all_radio.setSizePolicy(sizePolicy)
        self.all_radio.setChecked(True)
        self.all_radio.setObjectName(_fromUtf8("all_radio"))
        self.horizontalLayout_8.addWidget(self.all_radio)
        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.current_radio = QtGui.QRadioButton(Attenuation)
        self.current_radio.setObjectName(_fromUtf8("current_radio"))
        self.horizontalLayout_8.addWidget(self.current_radio)
        spacerItem1 = QtGui.QSpacerItem(5, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.range_radio = QtGui.QRadioButton(Attenuation)
        self.range_radio.setObjectName(_fromUtf8("range_radio"))
        self.horizontalLayout_8.addWidget(self.range_radio)
        self.rangemin_spin = QtGui.QSpinBox(Attenuation)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangemin_spin.sizePolicy().hasHeightForWidth())
        self.rangemin_spin.setSizePolicy(sizePolicy)
        self.rangemin_spin.setMaximum(99999)
        self.rangemin_spin.setObjectName(_fromUtf8("rangemin_spin"))
        self.horizontalLayout_8.addWidget(self.rangemin_spin)
        self.label_5 = QtGui.QLabel(Attenuation)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_8.addWidget(self.label_5)
        self.rangemax_spin = QtGui.QSpinBox(Attenuation)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangemax_spin.sizePolicy().hasHeightForWidth())
        self.rangemax_spin.setSizePolicy(sizePolicy)
        self.rangemax_spin.setMinimumSize(QtCore.QSize(10, 0))
        self.rangemax_spin.setMaximum(99999)
        self.rangemax_spin.setObjectName(_fromUtf8("rangemax_spin"))
        self.horizontalLayout_8.addWidget(self.rangemax_spin)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.splitter = QtGui.QSplitter(Attenuation)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.instr_param_gbox = QtGui.QGroupBox(self.splitter)
        self.instr_param_gbox.setMinimumSize(QtCore.QSize(0, 20))
        self.instr_param_gbox.setTitle(_fromUtf8(""))
        self.instr_param_gbox.setObjectName(_fromUtf8("instr_param_gbox"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.instr_param_gbox)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.inst_param_layout = QtGui.QVBoxLayout()
        self.inst_param_layout.setObjectName(_fromUtf8("inst_param_layout"))
        self.verticalLayout_7.addLayout(self.inst_param_layout)
        self.samp_param_layout = QtGui.QVBoxLayout()
        self.samp_param_layout.setObjectName(_fromUtf8("samp_param_layout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.rectRadioButton = QtGui.QRadioButton(self.instr_param_gbox)
        self.rectRadioButton.setChecked(True)
        self.rectRadioButton.setObjectName(_fromUtf8("rectRadioButton"))
        self.horizontalLayout_2.addWidget(self.rectRadioButton)
        self.cylRadioButton = QtGui.QRadioButton(self.instr_param_gbox)
        self.cylRadioButton.setObjectName(_fromUtf8("cylRadioButton"))
        self.horizontalLayout_2.addWidget(self.cylRadioButton)
        self.polyRadioButton = QtGui.QRadioButton(self.instr_param_gbox)
        self.polyRadioButton.setObjectName(_fromUtf8("polyRadioButton"))
        self.horizontalLayout_2.addWidget(self.polyRadioButton)
        self.polyPointFileEdit = QtGui.QLineEdit(self.instr_param_gbox)
        self.polyPointFileEdit.setObjectName(_fromUtf8("polyPointFileEdit"))
        self.horizontalLayout_2.addWidget(self.polyPointFileEdit)
        self.polyPointFileOpenButton = QtGui.QPushButton(self.instr_param_gbox)
        self.polyPointFileOpenButton.setMaximumSize(QtCore.QSize(20, 16777215))
        self.polyPointFileOpenButton.setObjectName(_fromUtf8("polyPointFileOpenButton"))
        self.horizontalLayout_2.addWidget(self.polyPointFileOpenButton)
        self.samp_param_layout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_7.addLayout(self.samp_param_layout)
        self.graphs_gbox = QtGui.QGroupBox(self.splitter)
        self.graphs_gbox.setMinimumSize(QtCore.QSize(0, 20))
        self.graphs_gbox.setTitle(_fromUtf8(""))
        self.graphs_gbox.setObjectName(_fromUtf8("graphs_gbox"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.graphs_gbox)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.splitter_2 = QtGui.QSplitter(self.graphs_gbox)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.frame = QtGui.QFrame(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.exp_graphic = MatplotlibWidget(self.frame)
        self.exp_graphic.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exp_graphic.sizePolicy().hasHeightForWidth())
        self.exp_graphic.setSizePolicy(sizePolicy)
        self.exp_graphic.setMinimumSize(QtCore.QSize(0, 0))
        self.exp_graphic.setObjectName(_fromUtf8("exp_graphic"))
        self.verticalLayout_4.addWidget(self.exp_graphic)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lock_axis_check = QtGui.QCheckBox(self.frame)
        self.lock_axis_check.setObjectName(_fromUtf8("lock_axis_check"))
        self.horizontalLayout_3.addWidget(self.lock_axis_check)
        self.drawonly_check = QtGui.QCheckBox(self.frame)
        self.drawonly_check.setObjectName(_fromUtf8("drawonly_check"))
        self.horizontalLayout_3.addWidget(self.drawonly_check)
        self.autoclear_check = QtGui.QCheckBox(self.frame)
        self.autoclear_check.setChecked(True)
        self.autoclear_check.setObjectName(_fromUtf8("autoclear_check"))
        self.horizontalLayout_3.addWidget(self.autoclear_check)
        self.cleardrawing_button = QtGui.QPushButton(self.frame)
        self.cleardrawing_button.setObjectName(_fromUtf8("cleardrawing_button"))
        self.horizontalLayout_3.addWidget(self.cleardrawing_button)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_4.addWidget(self.label)
        self.pb_check = QtGui.QCheckBox(self.frame)
        self.pb_check.setChecked(True)
        self.pb_check.setObjectName(_fromUtf8("pb_check"))
        self.horizontalLayout_4.addWidget(self.pb_check)
        self.sb_check = QtGui.QCheckBox(self.frame)
        self.sb_check.setChecked(True)
        self.sb_check.setObjectName(_fromUtf8("sb_check"))
        self.horizontalLayout_4.addWidget(self.sb_check)
        self.sample_check = QtGui.QCheckBox(self.frame)
        self.sample_check.setChecked(True)
        self.sample_check.setObjectName(_fromUtf8("sample_check"))
        self.horizontalLayout_4.addWidget(self.sample_check)
        self.gvol_check = QtGui.QCheckBox(self.frame)
        self.gvol_check.setChecked(True)
        self.gvol_check.setObjectName(_fromUtf8("gvol_check"))
        self.horizontalLayout_4.addWidget(self.gvol_check)
        self.cor_check = QtGui.QCheckBox(self.frame)
        self.cor_check.setChecked(True)
        self.cor_check.setObjectName(_fromUtf8("cor_check"))
        self.horizontalLayout_4.addWidget(self.cor_check)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.gpoints_check = QtGui.QCheckBox(self.frame)
        self.gpoints_check.setChecked(True)
        self.gpoints_check.setObjectName(_fromUtf8("gpoints_check"))
        self.horizontalLayout_5.addWidget(self.gpoints_check)
        self.dcone_check = QtGui.QCheckBox(self.frame)
        self.dcone_check.setChecked(True)
        self.dcone_check.setObjectName(_fromUtf8("dcone_check"))
        self.horizontalLayout_5.addWidget(self.dcone_check)
        self.ifrac_check = QtGui.QCheckBox(self.frame)
        self.ifrac_check.setChecked(True)
        self.ifrac_check.setObjectName(_fromUtf8("ifrac_check"))
        self.horizontalLayout_5.addWidget(self.ifrac_check)
        self.dpattern_check = QtGui.QCheckBox(self.frame)
        self.dpattern_check.setChecked(True)
        self.dpattern_check.setObjectName(_fromUtf8("dpattern_check"))
        self.horizontalLayout_5.addWidget(self.dpattern_check)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_6 = QtGui.QLabel(self.frame)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_6.addWidget(self.label_6)
        self.opacity_edit = QtGui.QLineEdit(self.frame)
        self.opacity_edit.setObjectName(_fromUtf8("opacity_edit"))
        self.horizontalLayout_6.addWidget(self.opacity_edit)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_6.addWidget(self.label_2)
        self.colourScaleMin_edit = QtGui.QLineEdit(self.frame)
        self.colourScaleMin_edit.setObjectName(_fromUtf8("colourScaleMin_edit"))
        self.horizontalLayout_6.addWidget(self.colourScaleMin_edit)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_6.addWidget(self.label_3)
        self.colourScaleMax_edit = QtGui.QLineEdit(self.frame)
        self.colourScaleMax_edit.setObjectName(_fromUtf8("colourScaleMax_edit"))
        self.horizontalLayout_6.addWidget(self.colourScaleMax_edit)
        self.colourScaleAuto_check = QtGui.QCheckBox(self.frame)
        self.colourScaleAuto_check.setChecked(True)
        self.colourScaleAuto_check.setObjectName(_fromUtf8("colourScaleAuto_check"))
        self.horizontalLayout_6.addWidget(self.colourScaleAuto_check)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.frame_3 = QtGui.QFrame(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.frame_3)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.cor_graphic = MatplotlibWidget(self.frame_3)
        self.cor_graphic.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cor_graphic.sizePolicy().hasHeightForWidth())
        self.cor_graphic.setSizePolicy(sizePolicy)
        self.cor_graphic.setMinimumSize(QtCore.QSize(0, 0))
        self.cor_graphic.setObjectName(_fromUtf8("cor_graphic"))
        self.verticalLayout_6.addWidget(self.cor_graphic)
        self.verticalLayout_8.addWidget(self.splitter_2)
        self.verticalLayout_3.addWidget(self.splitter)

        self.retranslateUi(Attenuation)
        QtCore.QObject.connect(self.refresh_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Attenuation.Refresh)
        QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Attenuation.Save)
        QtCore.QObject.connect(self.loadButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Attenuation.Load)
        QtCore.QObject.connect(self.rectRadioButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Attenuation.SampleTypeChanged)
        QtCore.QObject.connect(self.cylRadioButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Attenuation.SampleTypeChanged)
        QtCore.QObject.connect(self.cleardrawing_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Attenuation.ClearDrawing)
        QtCore.QObject.connect(self.lock_axis_check, QtCore.SIGNAL(_fromUtf8("clicked()")), Attenuation.LockAxis_clicked)
        QtCore.QObject.connect(self.animate_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Attenuation.Animate)
        QtCore.QObject.connect(self.polyRadioButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Attenuation.SampleTypeChanged)
        QtCore.QObject.connect(self.polyPointFileOpenButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Attenuation.SelectPolyFile)
        QtCore.QMetaObject.connectSlotsByName(Attenuation)

    def retranslateUi(self, Attenuation):
        Attenuation.setWindowTitle(_translate("Attenuation", "Attenuation Correction", None))
        Attenuation.setTitle(_translate("Attenuation", "Attenuation Correction", None))
        self.saveButton.setText(_translate("Attenuation", "Save parameters", None))
        self.loadButton.setText(_translate("Attenuation", "Load parameters", None))
        self.refresh_button.setText(_translate("Attenuation", "Refresh", None))
        self.animate_button.setText(_translate("Attenuation", "Calculate and animate", None))
        self.allfiles_check.setText(_translate("Attenuation", "All Files", None))
        self.label_4.setText(_translate("Attenuation", "Datasets:", None))
        self.all_radio.setText(_translate("Attenuation", "All", None))
        self.current_radio.setText(_translate("Attenuation", "Current", None))
        self.range_radio.setText(_translate("Attenuation", "Range:", None))
        self.label_5.setText(_translate("Attenuation", "to", None))
        self.rectRadioButton.setText(_translate("Attenuation", "Rectangular", None))
        self.cylRadioButton.setText(_translate("Attenuation", "Cylindrical", None))
        self.polyRadioButton.setText(_translate("Attenuation", "Polygon", None))
        self.polyPointFileOpenButton.setText(_translate("Attenuation", "...", None))
        self.lock_axis_check.setText(_translate("Attenuation", "Lock axes", None))
        self.drawonly_check.setText(_translate("Attenuation", "Draw only", None))
        self.autoclear_check.setText(_translate("Attenuation", "Autoclear", None))
        self.cleardrawing_button.setText(_translate("Attenuation", "Clear", None))
        self.label.setText(_translate("Attenuation", "Show:", None))
        self.pb_check.setText(_translate("Attenuation", "Prim beam", None))
        self.sb_check.setText(_translate("Attenuation", "Sec beam", None))
        self.sample_check.setText(_translate("Attenuation", "Sample", None))
        self.gvol_check.setText(_translate("Attenuation", "Gauge vol", None))
        self.cor_check.setText(_translate("Attenuation", "CoR", None))
        self.gpoints_check.setText(_translate("Attenuation", "Gridpoints", None))
        self.dcone_check.setText(_translate("Attenuation", "Diffraction cone", None))
        self.ifrac_check.setText(_translate("Attenuation", "Attenuation Correction Coeff", None))
        self.dpattern_check.setText(_translate("Attenuation", "Diffraction patterns", None))
        self.label_6.setText(_translate("Attenuation", "Opacity:", None))
        self.opacity_edit.setText(_translate("Attenuation", "0.3", None))
        self.label_2.setText(_translate("Attenuation", "Colour scale: Min:", None))
        self.colourScaleMin_edit.setText(_translate("Attenuation", "0.0", None))
        self.label_3.setText(_translate("Attenuation", "Max:", None))
        self.colourScaleMax_edit.setText(_translate("Attenuation", "1.0", None))
        self.colourScaleAuto_check.setText(_translate("Attenuation", "Auto", None))

from matplotlibwidget import MatplotlibWidget
