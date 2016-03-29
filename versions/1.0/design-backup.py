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
        ccdcontroller.resize(496, 267)
        self.centralWidget = QtGui.QWidget(ccdcontroller)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.widget = QtGui.QWidget(self.centralWidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 461, 191))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.imtypeLabel = QtGui.QLabel(self.widget)
        self.imtypeLabel.setObjectName(_fromUtf8("imtypeLabel"))
        self.gridLayout.addWidget(self.imtypeLabel, 0, 1, 1, 1)
        self.exptimeLabel = QtGui.QLabel(self.widget)
        self.exptimeLabel.setObjectName(_fromUtf8("exptimeLabel"))
        self.gridLayout.addWidget(self.exptimeLabel, 0, 3, 1, 1)
        self.exptypeComboBox = QtGui.QComboBox(self.widget)
        self.exptypeComboBox.setObjectName(_fromUtf8("exptypeComboBox"))
        self.exptypeComboBox.addItem(_fromUtf8(""))
        self.exptypeComboBox.addItem(_fromUtf8(""))
        self.exptypeComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.exptypeComboBox, 1, 1, 1, 1)
        self.testimCheckBox = QtGui.QCheckBox(self.widget)
        self.testimCheckBox.setObjectName(_fromUtf8("testimCheckBox"))
        self.gridLayout.addWidget(self.testimCheckBox, 1, 2, 1, 1)
        self.exptimeDoubleSpinBox = QtGui.QDoubleSpinBox(self.widget)
        self.exptimeDoubleSpinBox.setSingleStep(0.5)
        self.exptimeDoubleSpinBox.setObjectName(_fromUtf8("exptimeDoubleSpinBox"))
        self.gridLayout.addWidget(self.exptimeDoubleSpinBox, 1, 3, 1, 1)
        self.imtitleLabel = QtGui.QLabel(self.widget)
        self.imtitleLabel.setObjectName(_fromUtf8("imtitleLabel"))
        self.gridLayout.addWidget(self.imtitleLabel, 2, 1, 1, 1)
        self.imtitleLineEdit = QtGui.QLineEdit(self.widget)
        self.imtitleLineEdit.setObjectName(_fromUtf8("imtitleLineEdit"))
        self.gridLayout.addWidget(self.imtitleLineEdit, 3, 1, 1, 3)
        self.resetButton = QtGui.QPushButton(self.widget)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.gridLayout.addWidget(self.resetButton, 4, 0, 2, 1)
        self.imfilenameLabel = QtGui.QLabel(self.widget)
        self.imfilenameLabel.setObjectName(_fromUtf8("imfilenameLabel"))
        self.gridLayout.addWidget(self.imfilenameLabel, 4, 1, 1, 1)
        self.imfilenameLineEdit = QtGui.QLineEdit(self.widget)
        self.imfilenameLineEdit.setReadOnly(True)
        self.imfilenameLineEdit.setObjectName(_fromUtf8("imfilenameLineEdit"))
        self.gridLayout.addWidget(self.imfilenameLineEdit, 5, 1, 1, 3)
        self.exposeButton = QtGui.QPushButton(self.widget)
        self.exposeButton.setObjectName(_fromUtf8("exposeButton"))
        self.gridLayout.addWidget(self.exposeButton, 0, 0, 2, 1)
        ccdcontroller.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(ccdcontroller)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 496, 22))
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
        QtCore.QMetaObject.connectSlotsByName(ccdcontroller)

    def retranslateUi(self, ccdcontroller):
        ccdcontroller.setWindowTitle(_translate("ccdcontroller", "ccdcontroller", None))
        self.imtypeLabel.setText(_translate("ccdcontroller", "Image Type:", None))
        self.exptimeLabel.setText(_translate("ccdcontroller", "Exposure Time:", None))
        self.exptypeComboBox.setItemText(0, _translate("ccdcontroller", "Exposure", None))
        self.exptypeComboBox.setItemText(1, _translate("ccdcontroller", "Dark", None))
        self.exptypeComboBox.setItemText(2, _translate("ccdcontroller", "Bias", None))
        self.testimCheckBox.setText(_translate("ccdcontroller", "Test Image", None))
        self.imtitleLabel.setText(_translate("ccdcontroller", "Image Title:", None))
        self.resetButton.setText(_translate("ccdcontroller", "Reset", None))
        self.imfilenameLabel.setText(_translate("ccdcontroller", "Image Filename:", None))
        self.exposeButton.setText(_translate("ccdcontroller", "Expose", None))
        self.menu_File.setTitle(_translate("ccdcontroller", "&File", None))
        self.actionExit.setText(_translate("ccdcontroller", "Exit", None))

