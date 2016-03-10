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

        ## These attributes handle autoincrement of filename
        self.curr_filename = ""

        ## Dictionary for image exposure mode
        self.modedict = {"Exposure" : "exp",
                         "Dark" : "dark",
                         "Bias" : "bias",
                         "Exposure Stack" : "expstack",
                         "Bias Stack" : "biasstack",
                         "Dark Stack" : "darkstack",
                         "Exposure Series" : "expseries",
                         "Dark Series" : "darkseries"}

        ## Connect signals and slots
        self.imtitleLineEdit.editingFinished.connect(self.setfilename)
        self.exposeButton.clicked.connect(self.expose)
        self.resetButton.clicked.connect(self.reset)
        self.testimCheckBox.toggled.connect(self.setfilename)
        self.exptypeComboBox.currentIndexChanged.connect(self.setfilename)
        self.directoryPushButton.clicked.connect(self.setdirectory)
        self.imnumSpinBox.valueChanged.connect(self.setfilename)
        
        ## Initialize controller
        ccdsetup.sta3800_off()
        ccdsetup.sta3800_setup()

    def reset(self):
        """Run initial commands to set up controller"""

        reply = QtGui.QMessageBox.question(self, 'Confirmation', 'Are you sure you want to reset the STA3800 controller?',
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessage.No)

        if reply == QtGui.QMessageBox.Yes:

            ## Reset defaults
            self.exposeButton.setEnabled(False)
            self.imtitleLineEdit.setText("")
            self.imfilenameLineEdit.setText("")
            self.innumSpinBox.setValue(0)
            self.curr_filename = ""
            ccdsetup.sta3800_off()
            ccdsetup.sta3800_setup()
            

    def setfilename(self):
        """Update and display filepath for the image file"""

        ## Get filename parameters
        filename = str(self.imtitleLineEdit.text())
        mode = self.modedict[str(self.exptypeComboBox.currentText())]
        im_num = self.imnumSpinBox.value()
        exptime = self.exptimeDoubleSpinBox.value()
        
        ## If test image, set filename to generic filename
        if self.testimCheckBox.isChecked():
            self.exposeButton.setEnabled(True)
            self.imfilenameLineEdit.setText(path.join(DATA_DIRECTORY,
                                                      "test.{0}.fits".format(mode)))
            return

        ## Else, if not empty string, build new filename
        elif filename != "":

            ## If filename changed, reset image number
            if self.curr_filename != filename:
                self.imnumSpinBox.setValue(0)

            self.exposeButton.setEnabled(True)
            self.imfilenameLineEdit.setText(path.join(DATA_DIRECTORY, "{0}.{1}.{2}s.{3}.fits".format(filename, mode, exptime, im_num)))
            self.curr_filename = filename
            return

        ## If empty turn off expose button and erase filename
        self.exposeButton.setEnabled(False)
        self.imfilenameLineEdit.setText("")

        
    def setdirectory(self):

        ## Have user select existing directory
        new_directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))

        ## If return is not NULL, set the DATA_DIRECTORY and update filename
        if new_directory:
            global DATA_DIRECTORY
            DATA_DIRECTORY = new_directory
            self.setfilename()
            self.statusLineEdit.setText("Data directory changed to {0}".format(new_directory))
        
                            
    def expose(self):
        """Perform the specified image exposure"""

        ## This will only work if in separate worker thread
#        self.statusLineEdit.setText("Starting exposure") 

        ## Get exposure parameters
        filepath = self.imfilenameLineEdit.text()
        mode = self.modedict[str(self.exptypeComboBox.currentText())]
        exptime = self.exptimeDoubleSpinBox.value()

        exposure.im_acq(mode, filepath, exptime)

        self.statusLineEdit.setText("Exposure {0} finished.".format(filepath))

        ## If auto increment turned on, change Image Number spin box
        if self.autoincCheckBox.isChecked():
            if not self.testimCheckBox.isChecked():
                im_num = self.imnumSpinBox.value()
                self.imnumSpinBox.setValue(im_num+1)
                self.setfilename()

        exposure.display(filepath)

    def scan(self):
        pass

    def updatevoltage(self):
        pass

    def setvoltage(self):
        pass

    def closeEvent(self, event):
        """Try to 

        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message', 
                                           quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        
def main():

    app = QtGui.QApplication(sys.argv)
    form = Controller()
    form.show()
    app.exec_()

if __name__ == "__main__":


    ## Change this to read from a config file

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
