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
import time

import design
import ccdsetup
import exposure
import restore

###############################################################################
##
##  Worker Thread Class
##
###############################################################################

class WorkerThread(QtCore.QThread):

    def __init__(self, func, args):
        super(WorkerThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)

class QtHandler(logging.Handler, object):

    def __init__(self, sigEmitter):
        super(QtHandler, self).__init__()
        self.sigEmitter = sigEmitter

    def emit(self, status):
        message = str(status.getMessage())
        self.sigEmitter.emit(QtCore.SIGNAL("logMsg(QString)"), message)
        
###############################################################################
##
##  Controller GUI Class
##
###############################################################################

class Controller(QtGui.QMainWindow, design.Ui_ccdcontroller):

    image_start = QtCore.pyqtSignal(int)
    image_taken = QtCore.pyqtSignal(int)
    seqnum_inc = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.setupUi(self)

        ## Set up Qt log handler
        logEmitter = QtCore.QObject()
        self.connect(logEmitter, QtCore.SIGNAL("logMsg(QString)"),
                     self.statusEdit.append)

        consoleHandler = QtHandler(logEmitter)
        self.logger = logging.getLogger("sLogger")
        self.logger.addHandler(consoleHandler)

        ## These attributes handle autoincrement of filename
        self.curr_title = ""

        ## Dictionary for image exposure mode
        self.modedict = {"Exposure" : "exp",
                         "Dark" : "dark",
                         "Bias" : "bias",
                         "Exposure Stack" : "exp",
                         "Bias Stack" : "bias",
                         "Dark Stack" : "dark",
                         "Exposure Series" : "exp",
                         "Dark Series" : "dark"}

        ## Signals and slots for thread testing
        self.thread = WorkerThread(self.expose, ())
        self.thread.started.connect(lambda: self.exposeButton.setEnabled(False))
        self.thread.finished.connect(lambda: self.exposeButton.setEnabled(True))

        ## Connect signals and slots for functions
        self.exposeButton.clicked.connect(self.thread.start)
        self.resetButton.clicked.connect(self.resetConfirm)
        self.exptypeComboBox.currentIndexChanged.connect(self.activate_ui)
        self.directoryPushButton.clicked.connect(self.editdirectory)
        self.imtitleLineEdit.editingFinished.connect(self.checkfilename)
        self.testimCheckBox.clicked.connect(self.checkfilename)
        self.shutdownButton.clicked.connect(self.close)
        self.filterToggleButton.toggled.connect(self.toggleFilter)

        ## Progress bar signals
        self.image_start.connect(self.resetProgressBar)
        self.image_taken.connect(self.updateProgressBar)
        self.seqnum_inc.connect(self.autoIncrement)
        
        ## Restore past GUI display settings and reset sta3800 controller
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
            DATA_DIRECTORY = "./"
        else:
            self.logger.info("GUI display widget values successfully restored.")
            self.activate_ui()

    def resetConfirm(self):
        """Prompt for confirmation from user to reset the controller."""

        ## Check if exposure is in progress
        if self.thread.isRunning():
            QtGui.QMessageBox.warning(self, "Exposure warning.", "Exposure in progress, unable to close program.", QtGui.QMessageBox.Ok)
            return

        else:
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

    def checkfilename(self):

        title = str(self.imtitleLineEdit.text())

        if self.testimCheckBox.isChecked():

            self.exposeButton.setEnabled(True)
            return

        elif title != "":

            self.exposeButton.setEnabled(True)
            self.curr_title = title

            return

        self.exposeButton.setEnabled(False)
        self.displaydirectory()

    def displaydirectory(self):
        """Display the Data Directory in the GUI."""
        self.imfilenameLineEdit.setText(DATA_DIRECTORY)
        
    def editdirectory(self):
        """Open prompt for user to select a new directory to save data."""

        ## Have user select existing directory
        new_directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory",
                                                                   '/home/lsst/Data/'))

        ## If return is not NULL, set the DATA_DIRECTORY and update filename
        if new_directory:

            try:
                os.makedirs(new_directory)
            except OSError:
                if not os.path.isdir(new_directory):
                    self.logger.exception("An error occurred while creating a new directory.")

            global DATA_DIRECTORY
            DATA_DIRECTORY = new_directory
            self.displaydirectory()
            self.logger.info("Data directory changed to {0}.".format(new_directory))

    def toggleFilter(self):

        if self.filterToggleButton.isChecked():
            self.filterToggleButton.setText("Filter")
            self.filterComboBox.setEnabled(True)
            self.monoSpinBox.setEnabled(False)
        else:
            self.filterToggleButton.setText("Monochromator")
            self.filterComboBox.setEnabled(False)
            self.monoSpinBox.setEnabled(True)

    @QtCore.pyqtSlot(int)
    def resetProgressBar(self, max):
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(max)

    @QtCore.pyqtSlot(int)
    def updateProgressBar(self, i):
        self.progressBar.setValue(i)

    @QtCore.pyqtSlot(int)
    def autoIncrement(self, seqnum_old):
        if self.autoincCheckBox.isChecked():
            self.imnumSpinBox.setValue(seqnum_old+1)

    def expose(self):
        """Execute a shell script to perform a measurement, depending on the desired
           exposure type."""

        ## Determine type of exposure (exp, series, stack)
        exptype = str(self.exptypeComboBox.currentText())
        mode = self.modedict[exptype]

        ## Get exposure parameters
        if mode == "bias":
            exptime = 0.0
        else:
            exptime = self.exptimeSpinBox.value()
        imcount = self.imstackSpinBox.value()
        seqnum = self.imnumSpinBox.value()
        mintime = self.minexpSpinBox.value()
        maxtime = self.maxexpSpinBox.value()
        step = self.tstepSpinBox.value()

        ## Determine filter kwargs
        if self.filterToggleButton.isChecked():
            kwargs = {'filter_name' : str(self.filterComboBox.currentText())}
        else:
            kwargs = {'monowl' : self.monoSpinBox.value()}

        if self.testimCheckBox.isChecked():
            title = 'test'
        else:
            title = str(self.imtitleLineEdit.text())

        ## Build filepath
        filepath = os.path.join(str(self.imfilenameLineEdit.text()),title)
                                            
        ## Check if single exposure
        if exptype in ["Exposure", "Dark", "Bias"]:

            ## Perform exposure
            self.logger.info("Starting {0}s {1} image.".format(exptime, exptype))
            self.image_start.emit(1)

            try:
                print kwargs
                filename = exposure.im_acq(mode, filepath, exptime, seqnum, **kwargs)
                self.image_taken.emit(1)
            except subprocess.CalledProcessError:
                self.logger.exception("Error in executable {0}_acq. Image not taken.".format(mode))
            except OSError:
                self.logger.exception("Executable {0}_acq not found. Image not taken".format(mode))
            except IOError:
                self.logger.exception("File already exits. Image not taken.")
            else:
                self.logger.info("Exposure {0} finished successfully.".format(filename))
                self.seqnum_inc.emit(seqnum)
                subprocess.Popen(['ds9', '-mosaicimage', 'iraf', filename,
                                  '-zoom', 'to', 'fit', '-cmap', 'b'])

        ## Check if a stack of exposures of same type
        elif exptype in ["Exposure Stack", "Dark Stack", "Bias Stack"]:

            total = seqnum + imcount
            self.logger.info("Starting {0}s {1} stack.".format(exptime, exptype))
            self.image_start.emit(imcount)

            try:
                for i in range(seqnum, total):
                    self.logger.info("Starting image {0} of {1}.".format(i+1-seqnum, imcount))
                    filename = exposure.im_acq(mode, filepath, exptime, i, **kwargs)
                    self.logger.info("Exposure {0} finished successfully.".format(filename))
                    self.image_taken.emit(i+1-seqnum)
                    self.seqnum_inc.emit(i)
            except subprocess.CalledProcessError:
                self.logger.exception("Error in executable {0}_acq. Image not taken.".format(mode))
            except OSError:
                self.logger.exception("Executable {0}_acq not found. Image not taken.".format(mode))
            except IOError:
                self.logger.exception("File already exists. Image not taken.")
            else:
                self.logger.info("Exposure stack finished successfully.")
                subprocess.Popen(['ds9', '-mosaicimage', 'iraf', filename, '-zoom', 'to', 'fit', '-cmap', 'b'])
                
        ## Check if a series of exposures of increase exposure time
        elif exptype in ["Exposure Series", "Dark Series"]:

            ## Parameter checks
            if mintime > maxtime:
                self.logger.warning("Minimum time must be less than Maximum time. Series not started.")
                return
            elif step <= 0:
                self.logger.warning("Time step must be greater than 0. Series not started.")
                return

            ## Construct array of exposure times
            t = mintime
            time_array = []
            while t <= maxtime:
                time_array.append(t)
                t += step
                
            ## Perform series
            self.logger.info("Starting {0} series with mintime {1}, maxtime {2}, and step {3}.".format(exptype, mintime, maxtime, step))
            self.image_start.emit(len(time_array))
            
            try:
                for i, time in enumerate(time_array):
                    self.logger.info("Starting {0}s {1} image.".format(time, mode))
                    filename = exposure.im_acq(mode, filepath, time, seqnum, **kwargs)
                    self.logger.info("Exposure {0} finished successfully.".format(filename))
                    self.image_taken.emit(i+1)
            except subprocess.CalledProcessError:
                self.logger.exception("Error in executable {0}_acq. Image not taken.".format(mode))
            except OSError:
                self.logger.exception("Executable {0}_acq not found. Image not taken.".format(mode))
            except IOError:
                self.logger.exception("File already exists. Image not taken.")
            else:
                self.logger.info("Exposure series finished successfully.")
                subprocess.Popen(['ds9', '-mosaicimage', 'iraf', filename, '-zoom', 'to', 'fit', '-cmap', 'b'])
                self.seqnum_inc.emit(seqnum)
        
    def setvoltages(self):
        """Change the value of the specified voltages."""
        pass

    def activate_ui(self):
        """Activate and deactivate input widgets depending on the necessary arguments."""

        self.checkfilename()
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
            self.imnumSpinBox.setEnabled(True)
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

        ## Check if exposure in progress
        if self.thread.isRunning():
            QtGui.QMessageBox.warning(self, "Warning.", "Exposure in progress, unable to close program.", QtGui.QMessageBox.Ok)
            event.ignore()

        ## Confirmation dialog for 
        else:

            reply = QtGui.QMessageBox.question(self, 'Confirmation','Are you sure you want to shutdown the STA3800 controller?',
                                               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                               QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:          
                try:
                    self.settings.setValue("DATA_DIRECTORY", DATA_DIRECTORY)
                    restore.guisave(self, self.settings)
                except:
                    self.logger.warning("Failed to save settings to INI file.")
                event.accept()
            else:
                event.ignore()

###############################################################################
##
##  Main Functions
##
###############################################################################
        
def safe_shutdown():
    """Run controller shut off command after GUI is closed"""

    logger = logging.getLogger('sLogger')
    logger.handlers = [h for h in logger.handlers if not isinstance(h, QtHandler)]

    try:
        logger.info("Turning off sta3800 controller (sta3800_off).")
        ccdsetup.sta3800_off()
    except Exception:
        logger.exception("Unable to turn off controller! State may be unknown.")
    else:
        logger.info("Controller turned off successfully.")
        
def main():

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
