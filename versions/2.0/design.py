# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ccdcontroller.ui'
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

class Ui_ccdcontroller(object):
    def setupUi(self, ccdcontroller):
        ccdcontroller.setObjectName(_fromUtf8("ccdcontroller"))
        ccdcontroller.resize(876, 511)
        self.centralWidget = QtGui.QWidget(ccdcontroller)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.layoutWidget = QtGui.QWidget(self.centralWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 841, 431))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.mainGrid = QtGui.QGridLayout(self.layoutWidget)
        self.mainGrid.setMargin(11)
        self.mainGrid.setSpacing(6)
        self.mainGrid.setObjectName(_fromUtf8("mainGrid"))
        self.statusLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.statusLineEdit.setReadOnly(True)
        self.statusLineEdit.setObjectName(_fromUtf8("statusLineEdit"))
        self.mainGrid.addWidget(self.statusLineEdit, 1, 1, 1, 1)
        self.statusLabel = QtGui.QLabel(self.layoutWidget)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.mainGrid.addWidget(self.statusLabel, 1, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.layoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.mainGrid.addWidget(self.progressBar, 2, 1, 1, 1)
        self.tabWidget = QtGui.QTabWidget(self.layoutWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.exposurePage = QtGui.QWidget()
        self.exposurePage.setObjectName(_fromUtf8("exposurePage"))
        self.layoutWidget1 = QtGui.QWidget(self.exposurePage)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 0, 821, 301))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.exptimeSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.exptimeSpinBox.setEnabled(True)
        self.exptimeSpinBox.setReadOnly(False)
        self.exptimeSpinBox.setDecimals(1)
        self.exptimeSpinBox.setMaximum(100000.0)
        self.exptimeSpinBox.setSingleStep(0.5)
        self.exptimeSpinBox.setObjectName(_fromUtf8("exptimeSpinBox"))
        self.gridLayout.addWidget(self.exptimeSpinBox, 1, 5, 1, 1)
        self.imnumLabel = QtGui.QLabel(self.layoutWidget1)
        self.imnumLabel.setObjectName(_fromUtf8("imnumLabel"))
        self.gridLayout.addWidget(self.imnumLabel, 5, 2, 1, 1)
        self.exptypeComboBox = QtGui.QComboBox(self.layoutWidget1)
        self.exptypeComboBox.setObjectName(_fromUtf8("exptypeComboBox"))
        self.exptypeComboBox.addItem(_fromUtf8(""))
        self.exptypeComboBox.addItem(_fromUtf8(""))
        self.exptypeComboBox.addItem(_fromUtf8(""))
        self.exptypeComboBox.addItem(_fromUtf8(""))
        self.exptypeComboBox.addItem(_fromUtf8(""))
        self.exptypeComboBox.addItem(_fromUtf8(""))
        self.exptypeComboBox.addItem(_fromUtf8(""))
        self.exptypeComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.exptypeComboBox, 1, 2, 1, 1)
        self.minexpLabel = QtGui.QLabel(self.layoutWidget1)
        self.minexpLabel.setObjectName(_fromUtf8("minexpLabel"))
        self.gridLayout.addWidget(self.minexpLabel, 3, 5, 1, 1)
        self.maxexpLabel = QtGui.QLabel(self.layoutWidget1)
        self.maxexpLabel.setObjectName(_fromUtf8("maxexpLabel"))
        self.gridLayout.addWidget(self.maxexpLabel, 3, 6, 1, 1)
        self.directoryPushButton = QtGui.QPushButton(self.layoutWidget1)
        self.directoryPushButton.setObjectName(_fromUtf8("directoryPushButton"))
        self.gridLayout.addWidget(self.directoryPushButton, 1, 0, 1, 1)
        self.exptimeLabel = QtGui.QLabel(self.layoutWidget1)
        self.exptimeLabel.setObjectName(_fromUtf8("exptimeLabel"))
        self.gridLayout.addWidget(self.exptimeLabel, 0, 5, 1, 1)
        self.minexpSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.minexpSpinBox.setDecimals(1)
        self.minexpSpinBox.setObjectName(_fromUtf8("minexpSpinBox"))
        self.gridLayout.addWidget(self.minexpSpinBox, 4, 5, 1, 1)
        self.tstepLabel = QtGui.QLabel(self.layoutWidget1)
        self.tstepLabel.setObjectName(_fromUtf8("tstepLabel"))
        self.gridLayout.addWidget(self.tstepLabel, 5, 5, 1, 1)
        self.testimCheckBox = QtGui.QCheckBox(self.layoutWidget1)
        self.testimCheckBox.setObjectName(_fromUtf8("testimCheckBox"))
        self.gridLayout.addWidget(self.testimCheckBox, 1, 3, 1, 1)
        self.resetButton = QtGui.QPushButton(self.layoutWidget1)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.gridLayout.addWidget(self.resetButton, 9, 0, 1, 1)
        self.imfilenameLabel = QtGui.QLabel(self.layoutWidget1)
        self.imfilenameLabel.setObjectName(_fromUtf8("imfilenameLabel"))
        self.gridLayout.addWidget(self.imfilenameLabel, 8, 2, 1, 1)
        self.imstackLabel = QtGui.QLabel(self.layoutWidget1)
        self.imstackLabel.setObjectName(_fromUtf8("imstackLabel"))
        self.gridLayout.addWidget(self.imstackLabel, 8, 5, 1, 1)
        self.vline_1 = QtGui.QFrame(self.layoutWidget1)
        self.vline_1.setFrameShape(QtGui.QFrame.VLine)
        self.vline_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.vline_1.setObjectName(_fromUtf8("vline_1"))
        self.gridLayout.addWidget(self.vline_1, 0, 1, 10, 1)
        self.autoincCheckBox = QtGui.QCheckBox(self.layoutWidget1)
        self.autoincCheckBox.setChecked(True)
        self.autoincCheckBox.setObjectName(_fromUtf8("autoincCheckBox"))
        self.gridLayout.addWidget(self.autoincCheckBox, 6, 3, 1, 1)
        self.tstepSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.tstepSpinBox.setDecimals(1)
        self.tstepSpinBox.setObjectName(_fromUtf8("tstepSpinBox"))
        self.gridLayout.addWidget(self.tstepSpinBox, 6, 5, 1, 1)
        self.exposeButton = QtGui.QPushButton(self.layoutWidget1)
        self.exposeButton.setEnabled(False)
        self.exposeButton.setObjectName(_fromUtf8("exposeButton"))
        self.gridLayout.addWidget(self.exposeButton, 0, 0, 1, 1)
        self.hline_1 = QtGui.QFrame(self.layoutWidget1)
        self.hline_1.setFrameShape(QtGui.QFrame.HLine)
        self.hline_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.hline_1.setObjectName(_fromUtf8("hline_1"))
        self.gridLayout.addWidget(self.hline_1, 2, 5, 1, 2)
        self.maxexpSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.maxexpSpinBox.setDecimals(1)
        self.maxexpSpinBox.setObjectName(_fromUtf8("maxexpSpinBox"))
        self.gridLayout.addWidget(self.maxexpSpinBox, 4, 6, 1, 1)
        self.imnumSpinBox = QtGui.QSpinBox(self.layoutWidget1)
        self.imnumSpinBox.setMinimum(1)
        self.imnumSpinBox.setMaximum(999)
        self.imnumSpinBox.setObjectName(_fromUtf8("imnumSpinBox"))
        self.gridLayout.addWidget(self.imnumSpinBox, 6, 2, 1, 1)
        self.imstackSpinBox = QtGui.QSpinBox(self.layoutWidget1)
        self.imstackSpinBox.setMinimum(1)
        self.imstackSpinBox.setMaximum(999)
        self.imstackSpinBox.setObjectName(_fromUtf8("imstackSpinBox"))
        self.gridLayout.addWidget(self.imstackSpinBox, 9, 5, 1, 1)
        self.imtypeLabel = QtGui.QLabel(self.layoutWidget1)
        self.imtypeLabel.setObjectName(_fromUtf8("imtypeLabel"))
        self.gridLayout.addWidget(self.imtypeLabel, 0, 2, 1, 1)
        self.imtitleLabel = QtGui.QLabel(self.layoutWidget1)
        self.imtitleLabel.setObjectName(_fromUtf8("imtitleLabel"))
        self.gridLayout.addWidget(self.imtitleLabel, 3, 2, 1, 1)
        self.hline_2 = QtGui.QFrame(self.layoutWidget1)
        self.hline_2.setFrameShape(QtGui.QFrame.HLine)
        self.hline_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.hline_2.setObjectName(_fromUtf8("hline_2"))
        self.gridLayout.addWidget(self.hline_2, 7, 5, 1, 2)
        self.vline_2 = QtGui.QFrame(self.layoutWidget1)
        self.vline_2.setFrameShape(QtGui.QFrame.VLine)
        self.vline_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.vline_2.setObjectName(_fromUtf8("vline_2"))
        self.gridLayout.addWidget(self.vline_2, 0, 4, 10, 1)
        self.imtitleLineEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.imtitleLineEdit.setObjectName(_fromUtf8("imtitleLineEdit"))
        self.gridLayout.addWidget(self.imtitleLineEdit, 4, 2, 1, 2)
        self.imfilenameLineEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.imfilenameLineEdit.setEnabled(False)
        self.imfilenameLineEdit.setReadOnly(True)
        self.imfilenameLineEdit.setObjectName(_fromUtf8("imfilenameLineEdit"))
        self.gridLayout.addWidget(self.imfilenameLineEdit, 9, 2, 1, 2)
        self.tabWidget.addTab(self.exposurePage, _fromUtf8(""))
        self.voltagePage = QtGui.QWidget()
        self.voltagePage.setObjectName(_fromUtf8("voltagePage"))
        self.layoutWidget2 = QtGui.QWidget(self.voltagePage)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 10, 821, 281))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget2)
        self.gridLayout_2.setMargin(11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.vddLabel = QtGui.QLabel(self.layoutWidget2)
        self.vddLabel.setObjectName(_fromUtf8("vddLabel"))
        self.gridLayout_2.addWidget(self.vddLabel, 0, 0, 1, 1)
        self.vodLabel = QtGui.QLabel(self.layoutWidget2)
        self.vodLabel.setObjectName(_fromUtf8("vodLabel"))
        self.gridLayout_2.addWidget(self.vodLabel, 0, 1, 1, 1)
        self.vogLabel = QtGui.QLabel(self.layoutWidget2)
        self.vogLabel.setObjectName(_fromUtf8("vogLabel"))
        self.gridLayout_2.addWidget(self.vogLabel, 0, 2, 1, 1)
        self.vrdLabel = QtGui.QLabel(self.layoutWidget2)
        self.vrdLabel.setObjectName(_fromUtf8("vrdLabel"))
        self.gridLayout_2.addWidget(self.vrdLabel, 0, 3, 1, 1)
        self.rghiLabel = QtGui.QLabel(self.layoutWidget2)
        self.rghiLabel.setObjectName(_fromUtf8("rghiLabel"))
        self.gridLayout_2.addWidget(self.rghiLabel, 0, 4, 1, 1)
        self.rgloLabel = QtGui.QLabel(self.layoutWidget2)
        self.rgloLabel.setObjectName(_fromUtf8("rgloLabel"))
        self.gridLayout_2.addWidget(self.rgloLabel, 0, 5, 1, 1)
        self.vddLineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.vddLineEdit.setReadOnly(True)
        self.vddLineEdit.setObjectName(_fromUtf8("vddLineEdit"))
        self.gridLayout_2.addWidget(self.vddLineEdit, 1, 0, 1, 1)
        self.vodLineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.vodLineEdit.setReadOnly(True)
        self.vodLineEdit.setObjectName(_fromUtf8("vodLineEdit"))
        self.gridLayout_2.addWidget(self.vodLineEdit, 1, 1, 1, 1)
        self.vogLineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.vogLineEdit.setReadOnly(True)
        self.vogLineEdit.setObjectName(_fromUtf8("vogLineEdit"))
        self.gridLayout_2.addWidget(self.vogLineEdit, 1, 2, 1, 1)
        self.vrdLineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.vrdLineEdit.setReadOnly(True)
        self.vrdLineEdit.setObjectName(_fromUtf8("vrdLineEdit"))
        self.gridLayout_2.addWidget(self.vrdLineEdit, 1, 3, 1, 1)
        self.rghiLineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.rghiLineEdit.setReadOnly(True)
        self.rghiLineEdit.setObjectName(_fromUtf8("rghiLineEdit"))
        self.gridLayout_2.addWidget(self.rghiLineEdit, 1, 4, 1, 1)
        self.rgloLineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.rgloLineEdit.setReadOnly(True)
        self.rgloLineEdit.setObjectName(_fromUtf8("rgloLineEdit"))
        self.gridLayout_2.addWidget(self.rgloLineEdit, 1, 5, 1, 1)
        self.setvddLabel = QtGui.QLabel(self.layoutWidget2)
        self.setvddLabel.setObjectName(_fromUtf8("setvddLabel"))
        self.gridLayout_2.addWidget(self.setvddLabel, 2, 0, 1, 1)
        self.setvodLabel = QtGui.QLabel(self.layoutWidget2)
        self.setvodLabel.setObjectName(_fromUtf8("setvodLabel"))
        self.gridLayout_2.addWidget(self.setvodLabel, 2, 1, 1, 1)
        self.setvogLabel = QtGui.QLabel(self.layoutWidget2)
        self.setvogLabel.setObjectName(_fromUtf8("setvogLabel"))
        self.gridLayout_2.addWidget(self.setvogLabel, 2, 2, 1, 1)
        self.setvrdLabel = QtGui.QLabel(self.layoutWidget2)
        self.setvrdLabel.setObjectName(_fromUtf8("setvrdLabel"))
        self.gridLayout_2.addWidget(self.setvrdLabel, 2, 3, 1, 1)
        self.setrghiLabel = QtGui.QLabel(self.layoutWidget2)
        self.setrghiLabel.setObjectName(_fromUtf8("setrghiLabel"))
        self.gridLayout_2.addWidget(self.setrghiLabel, 2, 4, 1, 1)
        self.setrgloLabel = QtGui.QLabel(self.layoutWidget2)
        self.setrgloLabel.setObjectName(_fromUtf8("setrgloLabel"))
        self.gridLayout_2.addWidget(self.setrgloLabel, 2, 5, 1, 1)
        self.vddSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.vddSpinBox.setDecimals(1)
        self.vddSpinBox.setSingleStep(0.5)
        self.vddSpinBox.setObjectName(_fromUtf8("vddSpinBox"))
        self.gridLayout_2.addWidget(self.vddSpinBox, 3, 0, 1, 1)
        self.vodSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.vodSpinBox.setDecimals(1)
        self.vodSpinBox.setSingleStep(0.5)
        self.vodSpinBox.setObjectName(_fromUtf8("vodSpinBox"))
        self.gridLayout_2.addWidget(self.vodSpinBox, 3, 1, 1, 1)
        self.vogSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.vogSpinBox.setDecimals(1)
        self.vogSpinBox.setSingleStep(0.5)
        self.vogSpinBox.setObjectName(_fromUtf8("vogSpinBox"))
        self.gridLayout_2.addWidget(self.vogSpinBox, 3, 2, 1, 1)
        self.vrdSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.vrdSpinBox.setDecimals(1)
        self.vrdSpinBox.setSingleStep(0.5)
        self.vrdSpinBox.setProperty("value", 0.0)
        self.vrdSpinBox.setObjectName(_fromUtf8("vrdSpinBox"))
        self.gridLayout_2.addWidget(self.vrdSpinBox, 3, 3, 1, 1)
        self.rghiSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.rghiSpinBox.setDecimals(1)
        self.rghiSpinBox.setObjectName(_fromUtf8("rghiSpinBox"))
        self.gridLayout_2.addWidget(self.rghiSpinBox, 3, 4, 1, 1)
        self.rgloSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.rgloSpinBox.setDecimals(1)
        self.rgloSpinBox.setObjectName(_fromUtf8("rgloSpinBox"))
        self.gridLayout_2.addWidget(self.rgloSpinBox, 3, 5, 1, 1)
        self.parhiLabel = QtGui.QLabel(self.layoutWidget2)
        self.parhiLabel.setObjectName(_fromUtf8("parhiLabel"))
        self.gridLayout_2.addWidget(self.parhiLabel, 4, 0, 1, 1)
        self.parloLabel = QtGui.QLabel(self.layoutWidget2)
        self.parloLabel.setObjectName(_fromUtf8("parloLabel"))
        self.gridLayout_2.addWidget(self.parloLabel, 4, 1, 1, 1)
        self.serhiLabel = QtGui.QLabel(self.layoutWidget2)
        self.serhiLabel.setObjectName(_fromUtf8("serhiLabel"))
        self.gridLayout_2.addWidget(self.serhiLabel, 4, 2, 1, 1)
        self.serloLabel = QtGui.QLabel(self.layoutWidget2)
        self.serloLabel.setObjectName(_fromUtf8("serloLabel"))
        self.gridLayout_2.addWidget(self.serloLabel, 4, 3, 1, 1)
        self.parhiLineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.parhiLineEdit.setReadOnly(True)
        self.parhiLineEdit.setObjectName(_fromUtf8("parhiLineEdit"))
        self.gridLayout_2.addWidget(self.parhiLineEdit, 5, 0, 1, 1)
        self.parloLineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.parloLineEdit.setReadOnly(True)
        self.parloLineEdit.setObjectName(_fromUtf8("parloLineEdit"))
        self.gridLayout_2.addWidget(self.parloLineEdit, 5, 1, 1, 1)
        self.serhiLineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.serhiLineEdit.setReadOnly(True)
        self.serhiLineEdit.setObjectName(_fromUtf8("serhiLineEdit"))
        self.gridLayout_2.addWidget(self.serhiLineEdit, 5, 2, 1, 1)
        self.serloLineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.serloLineEdit.setReadOnly(True)
        self.serloLineEdit.setObjectName(_fromUtf8("serloLineEdit"))
        self.gridLayout_2.addWidget(self.serloLineEdit, 5, 3, 1, 1)
        self.parhiSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.parhiSpinBox.setDecimals(1)
        self.parhiSpinBox.setObjectName(_fromUtf8("parhiSpinBox"))
        self.gridLayout_2.addWidget(self.parhiSpinBox, 6, 0, 1, 1)
        self.parloSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.parloSpinBox.setDecimals(1)
        self.parloSpinBox.setObjectName(_fromUtf8("parloSpinBox"))
        self.gridLayout_2.addWidget(self.parloSpinBox, 6, 1, 1, 1)
        self.serhiSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.serhiSpinBox.setDecimals(1)
        self.serhiSpinBox.setObjectName(_fromUtf8("serhiSpinBox"))
        self.gridLayout_2.addWidget(self.serhiSpinBox, 6, 2, 1, 1)
        self.serloSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget2)
        self.serloSpinBox.setDecimals(1)
        self.serloSpinBox.setObjectName(_fromUtf8("serloSpinBox"))
        self.gridLayout_2.addWidget(self.serloSpinBox, 6, 3, 1, 1)
        self.resetvoltageButton = QtGui.QPushButton(self.layoutWidget2)
        self.resetvoltageButton.setObjectName(_fromUtf8("resetvoltageButton"))
        self.gridLayout_2.addWidget(self.resetvoltageButton, 7, 2, 1, 2)
        self.setvoltageButton = QtGui.QPushButton(self.layoutWidget2)
        self.setvoltageButton.setObjectName(_fromUtf8("setvoltageButton"))
        self.gridLayout_2.addWidget(self.setvoltageButton, 7, 4, 1, 2)
        self.tabWidget.addTab(self.voltagePage, _fromUtf8(""))
        self.mainGrid.addWidget(self.tabWidget, 0, 0, 1, 3)
        ccdcontroller.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(ccdcontroller)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 876, 22))
        self.menuBar.setNativeMenuBar(True)
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menu_File = QtGui.QMenu(self.menuBar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        ccdcontroller.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(ccdcontroller)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        ccdcontroller.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(ccdcontroller)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        ccdcontroller.setStatusBar(self.statusBar)
        self.actionExit = QtGui.QAction(ccdcontroller)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menu_File.addAction(self.actionExit)
        self.menuBar.addAction(self.menu_File.menuAction())

        self.retranslateUi(ccdcontroller)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ccdcontroller)

    def retranslateUi(self, ccdcontroller):
        ccdcontroller.setWindowTitle(_translate("ccdcontroller", "ccdcontroller", None))
        self.statusLabel.setText(_translate("ccdcontroller", "Status:", None))
        self.imnumLabel.setText(_translate("ccdcontroller", "Image Number:", None))
        self.exptypeComboBox.setItemText(0, _translate("ccdcontroller", "Exposure", None))
        self.exptypeComboBox.setItemText(1, _translate("ccdcontroller", "Exposure Stack", None))
        self.exptypeComboBox.setItemText(2, _translate("ccdcontroller", "Exposure Series", None))
        self.exptypeComboBox.setItemText(3, _translate("ccdcontroller", "Dark", None))
        self.exptypeComboBox.setItemText(4, _translate("ccdcontroller", "Dark Stack", None))
        self.exptypeComboBox.setItemText(5, _translate("ccdcontroller", "Dark Series", None))
        self.exptypeComboBox.setItemText(6, _translate("ccdcontroller", "Bias", None))
        self.exptypeComboBox.setItemText(7, _translate("ccdcontroller", "Bias Stack", None))
        self.minexpLabel.setText(_translate("ccdcontroller", "Min Exposure Time", None))
        self.maxexpLabel.setText(_translate("ccdcontroller", "Max Exposure Time", None))
        self.directoryPushButton.setText(_translate("ccdcontroller", "Set Data Directory", None))
        self.exptimeLabel.setText(_translate("ccdcontroller", "Exposure Time:", None))
        self.tstepLabel.setText(_translate("ccdcontroller", "Time Step", None))
        self.testimCheckBox.setText(_translate("ccdcontroller", "Test Image", None))
        self.resetButton.setText(_translate("ccdcontroller", "Reset Controller", None))
        self.imfilenameLabel.setText(_translate("ccdcontroller", "Image Filebase:", None))
        self.imstackLabel.setText(_translate("ccdcontroller", "Image Count", None))
        self.autoincCheckBox.setText(_translate("ccdcontroller", "Auto Increment?", None))
        self.exposeButton.setText(_translate("ccdcontroller", "Expose", None))
        self.imtypeLabel.setText(_translate("ccdcontroller", "Image Type:", None))
        self.imtitleLabel.setText(_translate("ccdcontroller", "Image Title:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.exposurePage), _translate("ccdcontroller", "Exposure", None))
        self.vddLabel.setText(_translate("ccdcontroller", "VDD", None))
        self.vodLabel.setText(_translate("ccdcontroller", "VOD", None))
        self.vogLabel.setText(_translate("ccdcontroller", "VOG", None))
        self.vrdLabel.setText(_translate("ccdcontroller", "VRD", None))
        self.rghiLabel.setText(_translate("ccdcontroller", "RG HI", None))
        self.rgloLabel.setText(_translate("ccdcontroller", "RG LO", None))
        self.setvddLabel.setText(_translate("ccdcontroller", "Set VDD", None))
        self.setvodLabel.setText(_translate("ccdcontroller", "Set VOD", None))
        self.setvogLabel.setText(_translate("ccdcontroller", "Set VOG", None))
        self.setvrdLabel.setText(_translate("ccdcontroller", "Set VRD", None))
        self.setrghiLabel.setText(_translate("ccdcontroller", "Set RG HI", None))
        self.setrgloLabel.setText(_translate("ccdcontroller", "Set RG LO", None))
        self.parhiLabel.setText(_translate("ccdcontroller", "PAR HI", None))
        self.parloLabel.setText(_translate("ccdcontroller", "PAR LO", None))
        self.serhiLabel.setText(_translate("ccdcontroller", "SER HI", None))
        self.serloLabel.setText(_translate("ccdcontroller", "SER LO", None))
        self.resetvoltageButton.setText(_translate("ccdcontroller", "Reset To Defaults", None))
        self.setvoltageButton.setText(_translate("ccdcontroller", "Set Voltages", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.voltagePage), _translate("ccdcontroller", "Voltages", None))
        self.menu_File.setTitle(_translate("ccdcontroller", "&File", None))
        self.actionExit.setText(_translate("ccdcontroller", "Exit", None))

