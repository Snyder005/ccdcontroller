#!/usr/bin/env python

from PyQt4 import QtGui
import sys
from os import path

import design
import ccdsetup

DATA_DIRECTORY = "./"

###############################################################################

class Controller(QtGui.QMainWindow, design.Ui_ccdcontroller):

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.setupUi(self)
        self.exposeButton.setEnabled(False) # Move to ui

        ## Connect signals and slots
        self.imtitleLineEdit.editingFinished.connect(self.setfilename)
        self.exposeButton.clicked.connect(self.expose)
        self.resetButton.clicked.connect(self.reset)
        self.testimCheckBox.toggled.connect(self.setfilename)
        
        ## Initialize controller
        print "ccd_auto.sta3800_setup()"

    def reset(self):

        print "ccd_auto.sta3800_setup()"
            

    def setfilename(self):
        """Update and display filepath for the image file"""

        filename = str(self.imtitleLineEdit.text())
        
        if self.testimCheckBox.isChecked():
            self.exposeButton.setEnabled(True)
            self.imfilenameLineEdit.setText(path.join(DATA_DIRECTORY,
                                            "test.fits"))
            return
        elif filename != "":
            self.exposeButton.setEnabled(True)
            self.imfilenameLineEdit.setText(path.join(DATA_DIRECTORY,
                                            "{}.fits".format(filename)))
            return

        self.exposeButton.setEnabled(False)
        self.imfilenameLineEdit.setText("")

    def expose(self):
        """Perform the specified image exposure"""

        modedict = {"Exposure" : "exp",
                    "Dark" : "dark",
                    "Bias" : "bias"}

        ## If test image, set filename to test.fits
        if self.testimCheckBox.isChecked():
            filepath = path.join(DATA_DIRECTORY, "test.fits")
        else:
            filepath = self.imfilenameLineEdit.text()

        mode = modedict[str(self.exptypeComboBox.currentText())]
        exptime = self.exptimeDoubleSpinBox.value()

        #img_acq(mode, filepath, exptime)
        print "img_acq({0}, {1}, {2}".format(mode, filepath, exptime)
        
def main():

    app = QtGui.QApplication(sys.argv)
    form = Controller()
    form.show()
    app.exec_()

if __name__ == "__main__":

    main()
