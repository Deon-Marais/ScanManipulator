# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Output\FiguresGUI.ui'
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

class Ui_Figures(object):
    def setupUi(self, Figures):
        Figures.setObjectName(_fromUtf8("Figures"))
        Figures.resize(410, 508)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Figures.sizePolicy().hasHeightForWidth())
        Figures.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Figures)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.allfiles_check = QtGui.QCheckBox(Figures)
        self.allfiles_check.setObjectName(_fromUtf8("allfiles_check"))
        self.horizontalLayout.addWidget(self.allfiles_check)
        self.label = QtGui.QLabel(Figures)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.all_radio = QtGui.QRadioButton(Figures)
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
        self.current_radio = QtGui.QRadioButton(Figures)
        self.current_radio.setObjectName(_fromUtf8("current_radio"))
        self.horizontalLayout.addWidget(self.current_radio)
        spacerItem1 = QtGui.QSpacerItem(5, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.range_radio = QtGui.QRadioButton(Figures)
        self.range_radio.setObjectName(_fromUtf8("range_radio"))
        self.horizontalLayout.addWidget(self.range_radio)
        self.rangemin_spin = QtGui.QSpinBox(Figures)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangemin_spin.sizePolicy().hasHeightForWidth())
        self.rangemin_spin.setSizePolicy(sizePolicy)
        self.rangemin_spin.setMaximum(99999)
        self.rangemin_spin.setObjectName(_fromUtf8("rangemin_spin"))
        self.horizontalLayout.addWidget(self.rangemin_spin)
        self.label_2 = QtGui.QLabel(Figures)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.rangemax_spin = QtGui.QSpinBox(Figures)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangemax_spin.sizePolicy().hasHeightForWidth())
        self.rangemax_spin.setSizePolicy(sizePolicy)
        self.rangemax_spin.setMinimumSize(QtCore.QSize(10, 0))
        self.rangemax_spin.setMaximum(99999)
        self.rangemax_spin.setObjectName(_fromUtf8("rangemax_spin"))
        self.horizontalLayout.addWidget(self.rangemax_spin)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget = QtGui.QTabWidget(Figures)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.dockWidget = QtGui.QDockWidget(self.tab_3)
        self.dockWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.dockWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.p2_scan_combo = QtGui.QComboBox(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p2_scan_combo.sizePolicy().hasHeightForWidth())
        self.p2_scan_combo.setSizePolicy(sizePolicy)
        self.p2_scan_combo.setObjectName(_fromUtf8("p2_scan_combo"))
        self.gridLayout.addWidget(self.p2_scan_combo, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(10, 0))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.p1_scan_combo = QtGui.QComboBox(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p1_scan_combo.sizePolicy().hasHeightForWidth())
        self.p1_scan_combo.setSizePolicy(sizePolicy)
        self.p1_scan_combo.setObjectName(_fromUtf8("p1_scan_combo"))
        self.gridLayout.addWidget(self.p1_scan_combo, 0, 0, 1, 1)
        self.graphadd_button = QtGui.QPushButton(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphadd_button.sizePolicy().hasHeightForWidth())
        self.graphadd_button.setSizePolicy(sizePolicy)
        self.graphadd_button.setMinimumSize(QtCore.QSize(20, 0))
        self.graphadd_button.setObjectName(_fromUtf8("graphadd_button"))
        self.gridLayout.addWidget(self.graphadd_button, 0, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.graph_scan = MatplotlibWidget(self.dockWidgetContents)
        self.graph_scan.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.graph_scan.setObjectName(_fromUtf8("graph_scan"))
        self.verticalLayout_2.addWidget(self.graph_scan)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton_3 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.apply_button = QtGui.QPushButton(self.dockWidgetContents)
        self.apply_button.setObjectName(_fromUtf8("apply_button"))
        self.horizontalLayout_3.addWidget(self.apply_button)
        spacerItem2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.pushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.verticalLayout_3.addWidget(self.dockWidget)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.dockWidget_2 = QtGui.QDockWidget(self.tab_4)
        self.dockWidget_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.dockWidget_2.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget_2.setObjectName(_fromUtf8("dockWidget_2"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_4 = QtGui.QLabel(self.dockWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(10, 0))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        self.waterfall_scan_combo = QtGui.QComboBox(self.dockWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waterfall_scan_combo.sizePolicy().hasHeightForWidth())
        self.waterfall_scan_combo.setSizePolicy(sizePolicy)
        self.waterfall_scan_combo.setMinimumSize(QtCore.QSize(80, 0))
        self.waterfall_scan_combo.setObjectName(_fromUtf8("waterfall_scan_combo"))
        self.horizontalLayout_5.addWidget(self.waterfall_scan_combo)
        self.apply_waterfall_button = QtGui.QPushButton(self.dockWidgetContents_2)
        self.apply_waterfall_button.setObjectName(_fromUtf8("apply_waterfall_button"))
        self.horizontalLayout_5.addWidget(self.apply_waterfall_button)
        self.pushButton_4 = QtGui.QPushButton(self.dockWidgetContents_2)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_5.addWidget(self.pushButton_4)
        self.pushButton_5 = QtGui.QPushButton(self.dockWidgetContents_2)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_5.addWidget(self.pushButton_5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.interp_check = QtGui.QCheckBox(self.dockWidgetContents_2)
        self.interp_check.setChecked(False)
        self.interp_check.setObjectName(_fromUtf8("interp_check"))
        self.gridLayout_2.addWidget(self.interp_check, 0, 2, 1, 1)
        self.ypts_edit = QtGui.QLineEdit(self.dockWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ypts_edit.sizePolicy().hasHeightForWidth())
        self.ypts_edit.setSizePolicy(sizePolicy)
        self.ypts_edit.setMinimumSize(QtCore.QSize(20, 0))
        self.ypts_edit.setObjectName(_fromUtf8("ypts_edit"))
        self.gridLayout_2.addWidget(self.ypts_edit, 0, 6, 1, 1)
        self.label_5 = QtGui.QLabel(self.dockWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 3, 1, 1)
        self.xpts_edit = QtGui.QLineEdit(self.dockWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xpts_edit.sizePolicy().hasHeightForWidth())
        self.xpts_edit.setSizePolicy(sizePolicy)
        self.xpts_edit.setMinimumSize(QtCore.QSize(20, 0))
        self.xpts_edit.setObjectName(_fromUtf8("xpts_edit"))
        self.gridLayout_2.addWidget(self.xpts_edit, 0, 4, 1, 1)
        self.label_6 = QtGui.QLabel(self.dockWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 0, 5, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.dockWidgetContents_2)
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 7, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.waterfall_layout = QtGui.QVBoxLayout()
        self.waterfall_layout.setObjectName(_fromUtf8("waterfall_layout"))
        self.widget = QtGui.QWidget(self.dockWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.waterfall_layout.addWidget(self.widget)
        self.verticalLayout_4.addLayout(self.waterfall_layout)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        self.verticalLayout_5.addWidget(self.dockWidget_2)
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Figures)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.apply_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Figures.ApplyFigure)
        QtCore.QObject.connect(self.graphadd_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Figures.GraphAdd)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Figures.Clear)
        QtCore.QObject.connect(self.graph_scan, QtCore.SIGNAL(_fromUtf8("customContextMenuRequested(QPoint)")), Figures.ApplyFigure)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), Figures.Refresh)
        QtCore.QObject.connect(self.apply_waterfall_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Figures.ApplyWaterfall)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), Figures.FileOpen)
        QtCore.QObject.connect(self.pushButton_5, QtCore.SIGNAL(_fromUtf8("clicked()")), Figures.FileSave)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), Figures.Clear3D)
        QtCore.QMetaObject.connectSlotsByName(Figures)

    def retranslateUi(self, Figures):
        Figures.setWindowTitle(_translate("Figures", "Excel", None))
        Figures.setTitle(_translate("Figures", "Figures Output", None))
        self.allfiles_check.setText(_translate("Figures", "All Files", None))
        self.label.setText(_translate("Figures", "Datasets:", None))
        self.all_radio.setText(_translate("Figures", "All", None))
        self.current_radio.setText(_translate("Figures", "Current", None))
        self.range_radio.setText(_translate("Figures", "Range:", None))
        self.label_2.setText(_translate("Figures", "to", None))
        self.dockWidget.setWindowTitle(_translate("Figures", "Scan parameters", None))
        self.label_3.setText(_translate("Figures", "vs.", None))
        self.graphadd_button.setText(_translate("Figures", "Add", None))
        self.pushButton_3.setText(_translate("Figures", "Refresh", None))
        self.apply_button.setText(_translate("Figures", "Apply", None))
        self.pushButton.setText(_translate("Figures", "Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Figures", "Scan", None))
        self.dockWidget_2.setWindowTitle(_translate("Figures", "Waterfall plot", None))
        self.label_4.setText(_translate("Figures", "vs.", None))
        self.apply_waterfall_button.setText(_translate("Figures", "Apply", None))
        self.pushButton_4.setText(_translate("Figures", "Open", None))
        self.pushButton_5.setText(_translate("Figures", "Save", None))
        self.interp_check.setText(_translate("Figures", "Interpolate", None))
        self.ypts_edit.setText(_translate("Figures", "100", None))
        self.label_5.setText(_translate("Figures", "x pts:", None))
        self.xpts_edit.setText(_translate("Figures", "100", None))
        self.label_6.setText(_translate("Figures", "y pts:", None))
        self.pushButton_2.setText(_translate("Figures", "Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Figures", "Waterfall", None))

from matplotlibwidget import MatplotlibWidget
