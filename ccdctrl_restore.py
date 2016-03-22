#!/usr/bin/env python

from PyQt4 import QtGui, QtCore
import sys
import argparse
from os import path
import os
import atexit

import design
import ccdsetup
import exposure
import restore

###############################################################################

class Controller(QtGui.QMainWindow, design.Ui_ccdcontroller):

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.setupUi(self)

        ## These attributes handle autoincrement of filename
        self.curr_filename = "" # add to settings

        ## Dictionary for image exposure mode
        self.modedict = {"Exposure" : "exp",
                         "Dark" : "dark",
                         "Bias" : "bias",
                         "Exposure Stack" : "exp",
                         "Bias Stack" : "bias",
                         "Dark Stack" : "dark",
                         "Exposure Series" : "exp",
                         "Dark Series" : "dark"}

        ## Connect signals and slots for functions
        self.exposeButton.clicked.connect(self.expose)
        self.resetButton.clicked.connect(self.reset)
        self.exptypeComboBox.currentIndexChanged.connect(self.activate_ui)
        self.directoryPushButton.clicked.connect(self.setdirectory)

        ## Connect signals to update filepath
        self.testimCheckBox.clicked.connect(self.setfilename)
        self.imtitleLineEdit.editingFinished.connect(self.setfilename)

        ## Restore past settings
        self.settings = QtCore.QSettings("LSST", "sta3800")

        global DATA_DIRECTORY
        DATA_DIRECTORY = unicode(self.settings.value("DATA_DIRECTORY").toString())

        restore.guirestore(self, self.settings)
        self.setfilename()
        self.activate_ui()

        self.statusLineEdit.setText("")
        
        ## Initialize controller
#        ccdsetup.sta3800_off()
#        ccdsetup.sta3800_setup()

    def reset(self):
        """Run initial commands to set up controller"""

        reply = QtGui.QMessageBox.question(self, 'Confirmation','Are you sure you want to reset the STA3800 controller?',
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:

            return

            ## Reset defaults
#            self.exposeButton.setEnabled(False)
#            self.imtitleLineEdit.setText("")
#            self.imfilenameLineEdit.setText("")
#            self.innumSpinBox.setValue(0)
#            self.curr_filename = ""
#            ccdsetup.sta3800_off()
#            ccdsetup.sta3800_setup()
            
    def setfilename(self):

        filename = str(self.imtitleLineEdit.text())
        mode = self.modedict[str(self.exptypeComboBox.currentText())]

        if self.testimCheckBox.isChecked():

            self.exposeButton.setEnabled(True)
            self.imfilenameLineEdit.setText(path.join(DATA_DIRECTORY, "test"))
            
            return

        elif filename != "":

            self.exposeButton.setEnabled(True)
            self.imfilenameLineEdit.setText(path.join(DATA_DIRECTORY, 
                                                      filename))
            self.curr_filename = filename

            return

        self.exposeButton.setEnabled(False)
        self.imfilenameLineEdit.setText(DATA_DIRECTORY)
        
    def setdirectory(self):
        """Open prompt for user to select a new directory to save data."""

        ## Have user select existing directory
        new_directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))

        ## If return is not NULL, set the DATA_DIRECTORY and update filename
        if new_directory:
            global DATA_DIRECTORY
            DATA_DIRECTORY = new_directory
            self.setfilename()
            self.statusLineEdit.setText("Data directory changed to {0}".format(new_directory))

    def expose(self):
        """Execute a shell script to perform a measurement, depending on the desired
           exposure type."""

        # Add a try/except here to catch failures of the shell script

        ## Determine type of exposure (exp, series, stack)
        exptype = str(self.exptypeComboBox.currentText())
        mode = self.modedict[exptype]
        filebase = "{0}.{1}.{2}s".format(self.imfilenameLineEdit.text(),
                                         mode, self.exptimeSpinBox.value())
                                            
        ## Check if single exposure
        if exptype in ["Exposure", "Dark", "Bias"]:

            ## Get necessary arguments
            exptime = self.exptimeSpinBox.value()  
            filebase = "{0}.{1}.{2}s".format(self.imfilenameLineEdit.text(),
                                             mode, exptime)    

            ## Perform exposure
#            filename = exposure.im_acq(mode, filebase, exptime)
            self.statusLineEdit.setText("Exposure {0} finished.".format(filebase))

        ## Check if a stack of exposures of same type
        elif exptype in ["Exposure Stack", "Dark Stack", "Bias Stack"]:

            ## Get necessary arguments
            exptime = self.exptimeSpinBox.value()
            imcount = self.imstackSpinBox.value() # Make sure this is type(int)
            start = self.imnumSpinBox.value() # Make sure this is type(int)
            filebase = "{0}.{1}.{2}s".format(self.imfilenameLineEdit.text(),
                                             mode, exptime)

#            exposure.stack(mode, filebase, imcount, exptime, start)
            self.statusLineEdit.setText("Exposure stack {0} finished".format(filebase))

        ## Check if a series of exposures of increase exposure time
        elif exptype in ["Exposure Series", "Dark Series"]:

            ## Get necessary arguments
            mintime = self.minexpSpinBox.value()
            maxtime = self.maxexpSpinBox.value()
            step = self.tstepSpinBox.value()
            filebase = "{0}.{1}".format(self.imfilenameLineEdit.text(),
                                        mode)

            # Could add checks here for appropriate values
            if mintime > maxtime:
                self.statusLineEdit.setText("Min time must be less than Max time.")
                return
                                        
#            exposure.series(mode, filebase, mintime, maxtime, step)
            self.statusLineEdit.setText("Exposure series {0} finished".format(filebase))
        
    def setvoltages(self):
        """Change the value of the specified voltages."""
        pass

    def activate_ui(self):
        """Activate and deactivate input widgets depending on the necessary arguments."""

        exptype = str(self.exptypeComboBox.currentText())

        if exptype in ["Exposure Stack", "Dark Stack", "Bias Stack"]:
            self.imstackSpinBox.setEnabled(True)
            self.imnumSpinBox.setEnabled(True)
            self.minexpSpinBox.setEnabled(False)
            self.maxexpSpinBox.setEnabled(False)
            self.tstepSpinBox.setEnabled(False)

            if exptype == "Bias Stack":
                self.exptimeSpinBox.setEnabled(False)
            else:
                self.exptimeSpinBox.setEnabled(True)

        elif exptype in ["Exposure Series", "Dark Series"]:
            self.exptimeSpinBox.setEnabled(False)
            self.imstackSpinBox.setEnabled(False)
            self.imnumSpinBox.setEnabled(False)
            self.minexpSpinBox.setEnabled(True)
            self.maxexpSpinBox.setEnabled(True)
            self.tstepSpinBox.setEnabled(True)

        else:
            self.imstackSpinBox.setEnabled(False)
            self.imnumSpinBox.setEnabled(True)
            self.minexpSpinBox.setEnabled(False)
            self.maxexpSpinBox.setEnabled(False)
            self.tstepSpinBox.setEnabled(False)

            if exptype == "Bias":
                self.exptimeSpinBox.setEnabled(False)
            else:
                self.exptimeSpinBox.setEnabled(True)

    def closeEvent(self, event):
        """Try a basic confirmation.  Wish to eventually expand this to save settings."""

        self.settings.setValue("DATA_DIRECTORY", DATA_DIRECTORY)
        restore.guisave(self, self.settings)
        event.accept()
        
#        quit_msg = "Are you sure you want to exit the program?"
#        reply = QtGui.QMessageBox.question(self, 'Message', 
#                                          quit_msg, QtGui.QMessageBox.Yes,
#                                          QtGui.QMessageBox.No)
        
#        if reply == QtGui.QMessageBox.Yes:
#            #ccdsetup.sta3800_off()

            # Save settings to config file
#            settings = QtCore.QSettings("LSST", "sta3800") 
#            restore.guisave(self, settings)
#            event.accept()
#        else:
#            event.ignore()



def safe_shutdown():
    """Run controller shut off command after GUI is closed"""

    ccdsetup.sta3800_off()
        
def main():

    ## Set up GUI
    app = QtGui.QApplication(sys.argv)
    form = Controller()
    form.show()
    app.exec_()
    
    ## Shut down GUI
    #atexit.register(safe_shutdown)

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
