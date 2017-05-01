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
from itertools import product
import time
import numpy as np

import design
import ccdsetup
import exposure
import restore
import voltage

###############################################################################
##
##  Misc. Thread Class
##
###############################################################################

class WorkerThread(QtCore.QThread):
    """Allows for multiple threads to run at same time."""

    def __init__(self, func, args):
        super(WorkerThread, self).__init__()
        self.func = func
        self.args = args
        self.status = True

    def run(self):
        self.func(*self.args)

    @QtCore.pyqtSlot()
    def cancel(self):
        self.status = False

    def reboot(self):
        self.status = True

class QtHandler(logging.Handler, object):
    """Object to handle displaying log information to GUI."""

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

    ## PyQt signals
    image_start = QtCore.pyqtSignal(int)
    image_taken = QtCore.pyqtSignal()
    exposure_cancel = QtCore.pyqtSignal()
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

        ## Dictionary for image exposure mode
        self.modedict = {"Exposure" : "exp",
                         "Dark" : "dark",
                         "Bias" : "bias",
                         "Flat" : "flat",
                         "Fe55" : "fe55",
                         "Exposure Series" : "exp",
                         "Dark Series" : "dark",
                         "Voltage Scan" : "scan"}

        ## Dictionary holds voltage widget and value information
        self.voltage_dict = {"VOD" : (self.vodLineEdit, 0),
                            "VOG" : (self.vogLineEdit, 0),
                            "VRD" : (self.vrdLineEdit, 0),
                            "VDD" : (self.vddLineEdit, 0),
                            "RGHI" : (self.rghiLineEdit, 0),
                            "RGLO" : (self.rgloLineEdit, 0),
                            "PARHI" : (self.parhiLineEdit, 0),
                            "PARLO" : (self.parloLineEdit, 0),
                            "SERHI" : (self.serhiLineEdit, 0),
                            "SERLO" : (self.serloLineEdit, 0)}

        ## Signals and slots for thread testing
        self.thread = WorkerThread(self.expose, ())
        self.thread.started.connect(lambda: self.exposeButton.setEnabled(False))
        self.thread.started.connect(lambda: self.cancelButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.exposeButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.cancelButton.setEnabled(False))
        self.exposure_cancel.connect(self.thread.cancel)
        self.exposeButton.clicked.connect(self.thread.start)

        ## Connect signals and slots for functions
        self.resetButton.clicked.connect(self.confirmReset)
        self.exptypeComboBox.currentIndexChanged.connect(self.setDisplay)
        self.directoryPushButton.clicked.connect(self.editDirectory)
        self.shutdownButton.clicked.connect(self.close)
        self.filterToggleButton.toggled.connect(self.toggleFilter)
        self.setvoltageButton.clicked.connect(lambda: self.setVoltages())
        self.cancelButton.clicked.connect(self.cancelExposure)
        self.paramfileButton.clicked.connect(self.editParamFile)

        ## Progress bar signals
        self.image_start.connect(self.resetProgressBar)
        self.image_taken.connect(self.updateProgressBar)
        self.seqnum_inc.connect(self.autoIncrement)
        
        ## Restore past GUI display settings and reset sta3800 controller
        self.restoreSettings()
        self.resetController()

    @QtCore.pyqtSlot(int)
    def autoIncrement(self, seqnum_old):
        """If auto-increment is on, increase Sequence Number by 1."""

        ## Auto-increment only if checked and not test image
        if self.autoincCheckBox.isChecked():
            if not self.testimCheckBox.isChecked():
                self.imnumSpinBox.setValue(seqnum_old+1)

    @QtCore.pyqtSlot()
    def cancelExposure(self):
        """Emit signal to cancel exposure."""

        self.logger.info("Finishing current exposure and canceling remaining exposures...")
        self.cancelButton.setEnabled(False)
        self.exposure_cancel.emit()

    @QtCore.pyqtSlot(int)
    def resetProgressBar(self, max):
        """Reset progress bar to 0, and initialize maximum."""

        self.progressBar.setValue(0)
        self.progressBar.setMaximum(max)

    @QtCore.pyqtSlot()
    def updateProgressBar(self):
        """Set new value of progress bar."""
        
        old_value = self.progressBar.value()
        self.progressBar.setValue(old_value+1)

    def setDisplay(self):
        """Activate and deactivate input widgets depending on exposure type."""

        exptype = str(self.exptypeComboBox.currentText())

        ## If a series of exposures, enable exptime limit input widgets
        if exptype in ["Exposure Series", "Dark Series"]:
            self.exptimeSpinBox.setEnabled(False)
            self.imstackSpinBox.setEnabled(False)
            self.imnumSpinBox.setEnabled(False)
            self.minexpSpinBox.setEnabled(True)
            self.maxexpSpinBox.setEnabled(True)
            self.tstepSpinBox.setEnabled(True)

        ## Else, disable series input widgets
        else:
            self.imstackSpinBox.setEnabled(True)
            self.imnumSpinBox.setEnabled(True)
            self.minexpSpinBox.setEnabled(False)
            self.maxexpSpinBox.setEnabled(False)
            self.tstepSpinBox.setEnabled(False)

            ## Bias has 0.0 exptime automatically
            if exptype == "Bias":
                self.exptimeSpinBox.setEnabled(False)
            else:
                self.exptimeSpinBox.setEnabled(True)

    def confirmReset(self):
        """Prompt user for confirmation to reset the controller."""

        ## Check if exposure is in progress, and if so, prevent reset
        if self.thread.isRunning():
            QtGui.QMessageBox.warning(self, "Exposure warning.",
                                      "Exposure in progress, unable to close program.",
                                      QtGui.QMessageBox.Ok)
            return

        ## Confirmation box for resetting controller
        else:
            reply = QtGui.QMessageBox.\
                    question(self, 'Confirmation',
                             'Are you sure you want to reset the STA3800 controller?',
                             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                             QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                self.reset()

    def editDirectory(self):
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

            global DATA_DIRECTORY
            DATA_DIRECTORY = new_directory
            self.imfilenameLineEdit.setText(DATA_DIRECTORY)
            self.logger.info("Data directory changed to {0}.".format(new_directory))

    def editParamFile(self):
        """Open prompt for user to select a parameter file for a voltage scan."""

        new_file = str(QtGui.QFileDialog.getOpenFileName(self, "Select File"))

        if new_file:

            self.paramfileLineEdit.setText(new_file)
            self.logger.info("Parameter file selected: {0}.".format(new_file))
                
    def expose(self):
        """Perform exposure using GUI parameters or parameters from file."""

        ## Build FITs header information
        kwargs = self.fitsinfo

        if self.filterToggleButton.isChecked():
            kwargs['filter_name'] = str(self.filterComboBox.currentText())
        else:
            kwargs['monowl'] = self.monoSpinBox.value()

        kwargs.update(self.getVoltageValues())

        ## Build filepath
        if self.testimCheckBox.isChecked():
            filename = 'test'
            kwargs['is_test'] = True
        else:
            filename = str(self.imtitleLineEdit.text())
            kwargs['is_test'] = False

        ## Get exposure parameters from GUI
        exptype = str(self.exptypeComboBox.currentText())
        mode = self.modedict[exptype]
        
        if mode == 'bias':
            exptime = 0.0
        else:
            exptime = self.exptimeSpinBox.value()
        num_images = self.imstackSpinBox.value()
        seq_num = self.imnumSpinBox.value()
        data_dir = DATA_DIRECTORY

        ## Exposure stack processing
        if exptype in ["Exposure", "Dark", "Bias", "Flat", "Fe55"]:
            
            ## Prep GUI for exposure
            self.image_start.emit(num_images)
            self.thread.reboot()

            ## Begin exposure stack
            for i in range(seq_num, seq_num+num_images):

                ## Check if stack interrupted
                if not self.thread.status:
                    self.logger.info("Exposure canceled.")
                    self.thread.reboot()
                    return

                ## Perform single exposure and check for errors
                try:
                    self.logger.info("Starting image {0} of {1}.".\
                                     format(i+1-seq_num, num_images))
                    filepath = exposure.im_acq(mode, filename, exptime, seq_num+i,
                                               data_dir, **kwargs)
                except subprocess.CalledProcessError:
                    self.logger.exception("Error in executable {0}_acq. Image not taken.".\
                                          format(mode))
                    return
                except OSError:
                    self.logger.exception("Executable {0}_acq not found. Image not taken.".\
                                          format(mode))
                    return
                except Exception as e:
                    self.logger.exception("{0}".format(e))
                    return
                else:
                    self.logger.info("Exposure finished successfully.")
                    self.image_taken.emit()
                    self.seqnum_inc.emit(i)

                ## Perform FITs header corrections
                try:
                    exposure.update_header(filepath)
                except IOError:
                    self.logger.exception("An error occurred while updating the FITs header.")

            else:
                self.logger.info("All exposures finished successfully.")
                #subprocess.Popen(['ds9', '-mosaicimage', 'iraf', filepath,
                #                  '-zoom', 'to', 'fit', '-cmap', 'b'])

        ## Exposure series processing
        elif exptype in ["Exposure Series", "Dark Series"]:

            ## Get additional GUI parameters
            mintime = self.minexpSpinBox.value()
            maxtime = self.maxexpSpinBox.value()
            timestep = self.tstepSpinBox.value()

            if mintime > maxtime:
                self.logger.warning("Minimum time must be less than Maximum time. " +
                                    "Series not started.")
                return
            elif timestep <= 0.0:
                self.logger.warning("Time step must be greater than 0. Series not started.")
                return

            ## Construct array of exposure times
            exptime = mintime
            exptimes = []
            while exptime <= maxtime:
                exptimes.append(exptime)
                exptime += timestep
            num_images = len(exptimes)

            ## Prepare GUI for exposure
            self.image_start.emit(num_images)
            self.thread.reboot()

            ## Begin exposure series
            for i, exptime in enumerate(exptimes):

                ## Check if series interrupted
                if not self.thread.status:
                    self.logger.info("Exposure series canceled.")
                    return

                ## Perform single exposure and check for errors
                try:
                    self.logger.info("Starting {0}s image.".format(exptime))
                    filepath = exposure.im_acq(mode, filename, exptime, seq_num,
                                               data_dir, **kwargs)
                except subprocess.CalledProcessError:
                    self.logger.exception("Error in executable {0}_acq. Image not taken.".\
                                          format(mode))
                    return
                except OSError:
                    self.logger.exception("Executable {0}_acq not found. Image not taken.".\
                                          format(mode))
                    return
                except Exception as e:
                    self.logger.exception("{0}".format(e))
                    return
                else:
                    self.logger.info("Exposure finished successfully.")
                    self.image_taken.emit()

                ## Perform FITs header corrections
                try:
                    exposure.update_header(filepath)

                except IOError:
                    self.logger.exception("An error occurred while updating the FITs header.")

            else:
                self.seqnum_inc.emit(seq_num)
                self.logger.info("All exposures finished successfully.")
                #subprocess.Popen(['ds9', '-mosaicimage', 'iraf', filepath,
                #                  '-zoom', 'to', 'fit', '-cmap', 'b'])

            
        elif exptype in ["Voltage Scan"]:

            ## Read file to get voltage parameters
            paramfile = str(self.paramfileLineEdit.text())

            with open(paramfile) as f:
                lines = f.readlines()

                values_list = []
                vnames = []

                for line in lines:
                    params = line.split()
                    vname = params[0]
                    values = list(np.arange(float(params[1]),
                                            float(params[2]),
                                            float(params[3])))

                    values_list.append(values)
                    vnames.append(vname)

            vpoints = list(product(*values_list))
            num_images = len(vpoints)

            self.image_start.emit(num_images)
            self.thread.reboot()

            for i, vpoint in enumerate(vpoints):

                if not self.thread.status:
                    self.logger.info("Exposure canceled.")
                    self.thread.reboot()
                    return
                
                new_voltage_dict = dict((vnames[j], vpoint[j]) for j in range(len(vnames)))
                self.setVoltages(new_voltage_dict, update_display=False)
                kwargs.update(new_voltage_dict)

                try:
                    self.logger.info("Starting exposure {0} of {1}.".format(i, num_images))
                    filepath = exposure.im_acq(mode, filename, exptime, 1, data_dir,
                                               **kwargs)
                except subprocess.CalledProcessError:
                    self.logger.exception("Error in executable. Image not taken.")
                    return
                except OSError:
                    self.logger.exception("Executable not found. Image not taken.")
                except Exception as e:
                    self.logger.exception("{0}".format(e))
                else:
                    self.logger.info("Exposure finished successfully.")
                    self.image_taken.emit()

                try:
                    exposure.update_header(filepath)
                except IOError:
                    self.logger.exception("An error occurred while updating the FITs header.")

            else:
                self.logger.info("All exposures finished successfully.")
                self.updateVoltageDisplay()
                                

    def resetController(self):
        """Perform controller off/on cycle (sta3800_off/sta3800_on)."""

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
            ## If controller reset cycle is succesful, set voltage values to nominal values
            self.defaultVoltages()
            self.logger.info("Controller turned on successfully.")
                                
    def restoreSettings(self):
        """Set GUI display widget values with values read from INI file."""

        global DATA_DIRECTORY

        try:

            ## Restore GUI display
            self.settings = QtCore.QSettings("./settings.ini", 
                                             QtCore.QSettings.IniFormat)
            DATA_DIRECTORY = unicode(self.settings.value("DATA_DIRECTORY").toString())
            restore.guirestore(self, self.settings)

            ## Restore FITs header settings
            self.fitsinfo = {}
            self.settings.beginGroup("Settings")
            for key in self.settings.childKeys():
                self.fitsinfo[str(key)] = str(self.settings.value(key).toString())
            self.settings.endGroup()
            
        except:
            self.logger.warning("Failed to restore past settings.")
            DATA_DIRECTORY = "./"
        else:
            self.logger.info("GUI display widget values successfully restored.")
            self.setDisplay()

    def toggleFilter(self):
        """Toggle filter choice (monochromator/broadband)."""

        if self.filterToggleButton.isChecked():
            self.filterToggleButton.setText("Filter")
            self.filterComboBox.setEnabled(True)
            self.monoSpinBox.setEnabled(False)
        else:
            self.filterToggleButton.setText("Monochromator")
            self.filterComboBox.setEnabled(False)
            self.monoSpinBox.setEnabled(True)

    def scan(self, filename, data_dir, *args, **kwargs):
        """Perform a scan over voltages provided by arguments."""

        ## Get voltage parameters
        vparams = args[0]
        vname = vparams[0]
        values = vparams[1]

        result = True

        ## Iterate through possible values
        for value in values:

            ## Check if scan interrupted
            if not self.thread.status:
                return False

            ## Update the voltage value
            new_voltage_dict = {vname : value}
            self.setVoltages(new_voltage_dict, update_display=False)
            kwargs[vname] = value

            ## If voltage arguments remain, create nested scan
            if len(args) > 1:
                result = self.scan(filename, data_dir, *args[1:], **kwargs)

            else:

                ## Perform a single exposure and check for errors
                self.logger.info("Starting EO Test exposures.")
                print "filepath = exposure.eotest_acq"
                time.sleep(1)
                raise OSError('Test')
                self.logger.info("Exposure finished successfully.")
                self.image_taken.emit()

                ## Perform FITs header corrections
                try:
                    print "exposure.update_header(filepath)"
                except IOError:
                    self.logger.exception("An error occurred while updating the FITs header.")

            if result is False:
                return False
                    
        return True
                    
    def setVoltages(self, new_voltage_dict=None, update_display=True):
        """Change the value of the specified voltages using an input dictionary."""

        ## If no voltage dictionary given, get values from GUI.
        if new_voltage_dict is None:
            new_voltage_dict = {str(self.voltageComboBox.currentText()) :
                                float(self.voltageSpinBox.value())}

        ## For each voltage, make call to executable
        for vname, value in new_voltage_dict.iteritems():

            if vname in ['VOD', 'VRD', 'VOG', 'VDD']:
                
                try:
                    output = voltage.set_voltage(value, vname)
                except subprocess.CalledProcessError:
                    self.logger.exception("Error in executable {0}." +
                                          " Voltage not changed.".format(vname))
                    break
                except OSError:
                    self.logger.exception("Executable {0} not found." +
                                          " Voltage not changed.".format(vname))
                    break
                else:
                    self.logger.info(output)
                    self.logger.info("Voltage {0} set to {1}".format(vname, value))
                    lineedit = self.voltage_dict[vname][0]
                    self.voltage_dict[vname] = (lineedit, value)

            ## Parallel clocks
            elif 'PAR' in vname:

                if 'LO' in vname:
                    par_lo = value
                    par_hi = self.voltage_dict['PARHI'][1]
                else:
                    par_lo = self.voltage_dict['PARLO'][1]
                    par_hi = value
            
                try:
                    output = voltage.par_clks(par_lo, par_hi)
                except subprocess.CalledProcessError:
                    self.logger.exception("Error in executable par_clks." +
                                          " Voltage not changed.")
                    break
                except OSError:
                    self.logger.exception("Executable par_clks not found." +
                                          " Voltage not changed.")
                    break
                else:
                    self.logger.info(output)
                    self.logger.info("Voltage {0} set to {1}".format(vname, value))
                    lineedit = self.voltage_dict[vname][0]
                    self.voltage_dict[vname] = (lineedit, value)

            ## Serial clocks
            elif 'SER' in vname:

                if 'LO' in vname:
                    ser_lo = value
                    ser_hi = self.voltage_dict['SERHI'][1]
                else:
                    ser_lo = self.voltage_dict['SERLO'][1]
                    ser_hi = value
            
                try:
                    output = voltage.ser_clks(ser_lo, ser_hi)
                except subprocess.CalledProcessError:
                    self.logger.exception("Error in executable ser_clks." +
                                          " Voltage not changed.")
                    break
                except OSError:
                    self.logger.exception("Executable ser_clks not found." +
                                          " Voltage not changed.")
                    break
                else:
                    self.logger.info(output)
                    self.logger.info("Voltage {0} set to {1}".format(vname, value))
                    lineedit = self.voltage_dict[vname][0]
                    self.voltage_dict[vname] = (lineedit, value)

            ## Reset clocks
            elif 'RG' in vname:

                if 'LO' in vname:
                    rg_lo = value
                    rg_hi = self.voltage_dict['RGHI'][1]
                else:
                    rg_lo = self.voltage_dict['RGLO'][1]
                    rg_hi = value
            
                try:
                    output = voltage.rg(rg_lo, rg_hi)
                except subprocess.CalledProcessError:
                    self.logger.exception("Error in executable rg. Voltage not changed.")
                    break
                except OSError:
                    self.logger.exception("Executable rg not found.  Voltage not changed.")
                    break
                else:
                    self.logger.info(output)
                    self.logger.info("Voltage {0} set to {1}".format(vname, value))
                    lineedit = self.voltage_dict[vname][0]
                    self.voltage_dict[vname] = (lineedit, value)

        ## Optionally update the display
        if update_display:
            self.updateVoltageDisplay()
            

    def updateVoltageDisplay(self):
        """Updates voltage displays with the current values."""

        for vname, vinfo in self.voltage_dict.iteritems():

            try:
                lineedit, value = vinfo
                lineedit.setText("{0:.2f}".format(value))
            except KeyError:
                self.logger.exception("No voltage matching {0} found!".format(vname))

    def defaultVoltages(self):
        """Sets voltage display to the default start-up voltages for controller."""

        ## Get default values from INI file
        self.settings.beginGroup("Voltages")
        voltage_keys = self.settings.childKeys()

        ## Set voltage dictionary to default values
        for key in voltage_keys:
            try:
                lineedit = self.voltage_dict[str(key)][0]
                self.voltage_dict[str(key)] = (lineedit,
                                               self.settings.value(key).toFloat()[0])

            except KeyError:
                self.logger.exception("No voltage matching {0} found!".format(str(key)))
        self.settings.endGroup()
        
        ## Update displays
        self.updateVoltageDisplay()

    def getVoltageValues(self):
        """Return voltage values as a dictionary."""

        voltage_dict = dict()
        for vname, vinfo in self.voltage_dict.iteritems():
            voltage_dict[vname] = float(vinfo[1])
        return voltage_dict

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
