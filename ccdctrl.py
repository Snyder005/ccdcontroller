#!/usr/bin/env python

from PyQt4 import QtGui, QtCore
import sys
import argparse
from os import path
import os
import atexit
import subprocess
import logging
from logging.config import fileConfig

import design
import ccdsetup
import exposure
import restore

###############################################################################

class Controller(QtGui.QMainWindow, design.Ui_ccdcontroller):

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.setupUi(self)
        self.logger = logging.getLogger("sLogger")

        ## These attributes handle autoincrement of filename
        self.curr_filename = ""

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
        self.resetButton.clicked.connect(self.resetConfirm)
        self.exptypeComboBox.currentIndexChanged.connect(self.activate_ui)
        self.directoryPushButton.clicked.connect(self.editdirectory)
        
        self.restoreGUI()
        self.reset()

    def restoreGUI(self):
        """Set GUI display widget values with values read from INI file."""

        global DATA_DIRECTORY

        try:
            self.settings = QtCore.QSettings("./settings.ini", 
                                             QtCore.QSettings.IniFormat)
            DATA_DIRECTORY = unicode(self.settings.value("DATA_DIRECTORY").toString())
            restore.guirestore(self, self.settings)
        except:
            self.logger.warning("Failed to restore past values for GUI display widgets.")
            self.statusEdit.setText("Warning: Failed to restore past settings.")
            DATA_DIRECTORY = "./"
        else:
            self.logger.info("GUI display widget values successfully restored.")

            self.displaydirectory()
            self.activate_ui()

    def resetConfirm(self):
        """Prompt for confirmation from user to reset the controller."""

        reply = QtGui.QMessageBox.question(self, 'Confirmation','Are you sure you want to reset the STA3800 controller?',
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.reset()

    def reset(self):
        """Turn off controller to bring to known state (sta3800_off), then turn on 
        controller (sta3800_on.)"""

        ## Turn off controller to bring to a known state
        try:
            self.logger.info("Turning off sta3800 controller (sta3800_off).")
            ccdsetup.sta3800_off()

        except Exception:
            self.logger.exception("Unable to turn off controller! State may be unknown.")
            raise
        else:
            self.logger.info("Controller turned off successfully.")

        ## Initialize controller
        try:
            self.logger.info("Turning on sta3800 controller (sta3800_setup).")
            ccdsetup.sta3800_setup()
        except Exception:
            self.logger.exception("Unable to turn on sta3800 controller!")
            raise
        else:
            self.logger.info("Controller turned on successfully.")

    def displaydirectory(self):
        """Display the Data Directory in the GUI."""
        self.imfilenameLineEdit.setText(DATA_DIRECTORY)
        
    def editdirectory(self):
        """Open prompt for user to select a new directory to save data."""

        ## Have user select existing directory
        new_directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))

        ## If return is not NULL, set the DATA_DIRECTORY and update filename
        if new_directory:

            try:
                os.makedirs(new_directory)
            except OSError:
                if not os.path.isdir(new_directory):
                    self.logger.exception("An error occurred while creating a new directory.")
                    self.statusEdit.setText("An error occurred while creating a new directory.")

            global DATA_DIRECTORY
            DATA_DIRECTORY = new_directory
            self.displaydirectory()
            self.logger.info("Data directory changed to {0}.".format(new_directory))
            self.statusEdit.setText("Data directory changed to {0}.".format(new_directory))

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
            if mode == "bias":
                exptime = 0.0
            else:
                exptime = self.exptimeSpinBox.value()
            filebase = "{0}.{1}.{2}s".format(self.imfilenameLineEdit.text(),
                                             mode, exptime)    

            ## Perform exposure
            self.logger.info("Starting {0}s {1} image with filebase {2}.".format(exptime,
                                                                                 exptype,
                                                                                 filebase))

            try:
                filename = exposure.im_acq(mode, filebase, exptime)
            except subprocess.CalledProcessError:
                self.logger.exception("Error in executable {0}_acq. Image not taken.".format(mode))
            except OSError:
                self.logger.exception("Exposure {0} finished successfully.".format(filename))
            except IOError:
                self.statusEdit.setText("File already exits. Image not taken.")
            else:
                self.logger.info("Exposure {0} finished successfully.".format(filename))
                self.statusEdit.setText("Exposure {0} finished.".format(filename))
                subprocess.Popen(['ds9', '-mosaicimage', 'iraf', filename, '-zoom', 'to', 'fit'])
                

        ## Check if a stack of exposures of same type
        elif exptype in ["Exposure Stack", "Dark Stack", "Bias Stack"]:

            ## Get necessary arguments
            if mode == "bias":
                exptime = 0.0
            else:
                exptime = self.exptimeSpinBox.value()
            imcount = self.imstackSpinBox.value() # Make sure this is type(int)
            start = self.imnumSpinBox.value() # Make sure this is type(int)
            filebase = "{0}.{1}.{2}s".format(self.imfilenameLineEdit.text(),
                                             mode, exptime)

            ## Perform stack
            self.logger.info("Starting {0} with imcount {1}, exptime {2}, and filebase {3}.".format(exptype, imcount, exptime, filebase))

            try:
                filename = exposure.stack(mode, filebase, imcount, exptime, start)
            except subprocess.CalledProcessError:
                self.logger.exception("Error in executable {0}_acq. Image not taken.".format(mode))
            except OSError:
                self.logger.exception("Executable {0}_acq not found. Image not taken.".format(mode))
            except IOError:
                self.statusEdit.setText("File already exitst. Image not taken.")
            else:
                self.logger.info("{0} finished successfully.".format(filebase))
                self.statusEdit.setText("Exposure stack {0} finished".format(filebase))
                subprocess.Popen(['ds9', '-mosaicimage', 'iraf', filename, '-zoom', 'to', 'fit'])
                

        ## Check if a series of exposures of increase exposure time
        elif exptype in ["Exposure Series", "Dark Series"]:

            ## Get necessary arguments
            mintime = self.minexpSpinBox.value()
            maxtime = self.maxexpSpinBox.value()
            step = self.tstepSpinBox.value()
            filebase = "{0}.{1}".format(self.imfilenameLineEdit.text(),
                                        mode)

            ## Parameter checks
            if mintime > maxtime:
                self.statusEdit.setText("Min time must be less than Max time.")
                return

            ## Perform series
            self.logger.info("Starting {0} with mintime {1}, maxtime {2}, step {3}, and filebase {4}.".format(exptype, mintime, maxtime, step, filebase))
            try:
                filename = exposure.series(mode, filebase, mintime, maxtime, step)
            except subprocess.CalledProcessError:
                self.logger.exception("Error in executable {0}_acq. Image not taken.".format(mode))
            except OSError:
                self.logger.exception("Executable {0}_acq not found. Image not taken.".format(mode))
            except IOError:
                self.statusEdit.setText("File already exitst. Image not taken.")
            else:
                self.logger.info("{0} finished successfully.".format(filebase))
                self.statusEdit.setText("Exposure series {0} finished".format(filebase))
                subprocess.Popen(['ds9', '-mosaicimage', 'iraf', filename, '-zoom', 'to', 'fit'])
        
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
        """Need to reconcile confirmation and guisave settings."""

        ## Save settings to INI file

        try:
            self.settings.setValue("DATA_DIRECTORY", DATA_DIRECTORY)
            restore.guisave(self, self.settings)
        except:
            self.logger.warning("Failed to save settings to INI file.")
            
        event.accept()

def safe_shutdown():
    """Run controller shut off command after GUI is closed"""

    logger = logging.getLogger('sLogger')

    try:
        logger.info("Turning off sta3800 controller (sta3800_off).")
        ccdsetup.sta3800_off()
    except Exception:
        logger.exception("Unable to turn off controller! State may be unknown.")
    else:
        logger.info("Controller turned off successfully.")
        
def main():

    ## Set up DS(
    
    #subprocess.Popen("ds9") ## Test if ds9 can be opened in background

    ## Set up logging
    fileConfig("settings.ini")
    logger = logging.getLogger('sLogger')

    ## Set up GUI
    app = QtGui.QApplication(sys.argv)
    form = Controller()
    form.show()
    app.exec_()
    
    ## Shut down GUI
    atexit.register(safe_shutdown)

if __name__ == "__main__":

    main()
