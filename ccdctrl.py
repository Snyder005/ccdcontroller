#!/usr/bin/env python

from PyQt4 import QtGui
import sys
import argparse
from os import path
import os

import design
import ccdsetup
import exposure

###############################################################################

class Controller(QtGui.QMainWindow, design.Ui_ccdcontroller):

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.setupUi(self)
        self.exposeButton.setEnabled(False) # Move to ui

        ## These attributes handle autoincrement of filename
        self.num_img = 0
        self.curr_filename = ""

        ## Dictionary for image exposure mode
        self.modedict = {"Exposure" : "exp",
                         "Dark" : "dark",
                         "Bias" : "bias"}

        ## Connect signals and slots
        self.imtitleLineEdit.editingFinished.connect(self.setfilename)
        self.exposeButton.clicked.connect(self.expose)
        self.resetButton.clicked.connect(self.reset)
        self.testimCheckBox.toggled.connect(self.setfilename)
        
        ## Initialize controller
        ccdsetup.sta3800_setup()

    def reset(self):
        """Run initial commands to set up controller"""

        self.exposeButton.setEnabled(False)
        self.imtitleLineEdit.setText("")
        self.imfilenameLineEdit.setText("")
        self.num_img = 0
        self.curr_filename = ""
        ccdsetup.sta3800_setup()
            

    def setfilename(self):
        """Update and display filepath for the image file"""

        filename = str(self.imtitleLineEdit.text())
        mode = self.modedict[str(self.exptypeComboBox.currentText())]
        
        if self.testimCheckBox.isChecked():
            self.exposeButton.setEnabled(True)
            self.imfilenameLineEdit.setText(path.join(DATA_DIRECTORY,
                                                      "test_{0}.fits".format(mode)))
            return
        elif filename != "":

            if self.curr_filename != filename:
                self.num_img = 0
            self.exposeButton.setEnabled(True)
            self.imfilenameLineEdit.setText(path.join(DATA_DIRECTORY, "{0}_{1}_{2}.fits".format(filename, mode, self.num_img)))
            self.curr_filename = filename
            return

        self.exposeButton.setEnabled(False)
        self.imfilenameLineEdit.setText("")

    def expose(self):
        """Perform the specified image exposure"""

        print "Starting exposure" # Send to some prompt on GUI

        ## If test image, set filename to test.fits
        if self.testimCheckBox.isChecked():
            filepath = path.join(DATA_DIRECTORY, "test.fits")
        else:
            filepath = self.imfilenameLineEdit.text()

        mode = self.modedict[str(self.exptypeComboBox.currentText())]
        exptime = self.exptimeDoubleSpinBox.value()

        #img_acq(mode, filepath, exptime)
        exposure.im_acq(mode, filepath, exptime)

        print "Finished exposure" # Same as above

        ## Autoincrement images
        self.num_img += 1
        self.setfilename()

    def scan(self):
        pass

    def updatevoltage(self):
        pass

    def setvoltage(self):
        pass
        
def main():

    app = QtGui.QApplication(sys.argv)
    form = Controller()
    form.show()
    app.exec_()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default = "./", 
                        help="Specify data directory")

    args = parser.parse_args()

    ## Set the global data directory

    global DATA_DIRECTORY
    DATA_DIRECTORY = args.directory

    ## Make directory if it does not exist
    try: 
        os.makedirs(DATA_DIRECTORY)
    except OSError:
        if not os.path.isdir(DATA_DIRECTORY):
            raise

    main()
