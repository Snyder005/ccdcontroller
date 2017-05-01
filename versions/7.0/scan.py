import exposure
import numpy as np

## test for invalid voltage names and values

def scan_params(filename):

    ## Set all voltages to default

    ## Read filename
    with open(filename) as f:
        lines = f.readlines()

        vparams_list = []
        
        for line in lines:
            params = line.split()

            vname = params[0]
            values = list(np.arange(float(params[1]),
                                    float(params[2]),
                                    float(params[3])))

            vparams_list.append((vname, values))

    return scan_params

class Controller():

    def expose():

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
        data_directory = DATA_DIRECTORY

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
                    logger.info("Starting image {0} of {1}.".format(i+1-seqnum, num_images))
                    #filepath = exposure.im_acq()
                except subprocess.CalledProcessError:
                    self.logger.exception("Error in executable {0}_acq. Image not taken."./
                                          format(mode))
                except OSError:
                    self.logger.exception("Executable {0}_acq not found. Image not taken."./
                                          format(mode))
                except IOError as e:
                    self.logger.exception("{0}".format(e))
                else:
                    self.logger.info("Exposure finished successfully.")
                    self.image_taken.emit(i+1-seqnum)
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
            elif step <= 0:
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
            for i, exptime = enumerate(exptimes):

                ## Check if series interrupted
                if not self.thread.status:
                    self.logger.info("Exposure canceled.")

                ## Perform single exposure and check for errors
                try:
                    self.logger.info("Starting {0}s image.".format(exptime))
                    #filepath = exposure.im_acq()
                except subprocess.CalledProcessError:
                    self.logger.exception("Error in executable {0}_acq. Image not taken."./
                                          format(mode))
                except OSError:
                    self.logger.exception("Executable {0}_acq not found. Image not taken."./
                                          format(mode))
                except IOError as e:
                    self.logger.exception("{0}".format(e))
                else:
                    self.logger.info("Exposure finished successfully.")
                    self.image_taken.emit(i+1-seqnum)
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

            
        elif exptype in ["Voltage Scan"]:
            pass

            ## Do stuff
    

def scan(filebase, *args):
    """Scan a range of voltages and make necessary characterization
    measurements.
    """
    
    ## Get first tuple of arguments and assign
    v_settings = args[0]
    
    v_name = v_settings[0]
    v_min = float(v_settings[1])
    v_max = float(v_settings[2])
    v_step = float(v_settings[3])

    print v_name, v_min, v_max, v_step

    ## Set up loop for the voltage
    volts = v_min
    
    while (volts < v_max):

        if canceled:
            ## raise error or emit signal
            return False

        print 'self.setVoltages({vname : volts}, update_display=False)'

        ## If voltages remain, run again with remaining sets of parameters
        if len(args) > 1:

            result = scan(filebase, *args[1:])

        ## If list is exhausted perform measurement and increment
        else:
            print v_name, volts

        ## If previous iteration was finished, continue
        if result is False:
            return False
        else:
            volts += v_step

    return True

def scan2(*args):

    vparams = args[0]
    
    vname = vparams[0]
    values = vparams[1]

    print vname, values

    canceled = False

    for value in values:

        ## Check if user has canceled the scan
        if canceled:
            return False

        print vname, value

        ## If voltage parameters remain, build another loop
        if len(args) > 1:

            ## Do iteration over next voltage parameters
            scan2(*args[1:])

        ## If no voltage parameters left, perform measurement
        else:
            print vname, value
            
    return True

    

if __name__ == '__main__':

   main('scan_test1.txt')
