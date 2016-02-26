#!/usr/bin/env python

"""
This is a Python script to make different exposure measurements
"""

import subprocess
import os
import errno

import voltage

from time import sleep

if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

###############################################################################
##
##  Voltage Scans
##
###############################################################################

def all_stack(dtime, imcount, filebase, fileend):
    """Perform all necessary measurements for CCD characterization"""

    bias_stack(imcount, "bias{0}".format(fileend))
    dark_stack(dtime, imcount, "dark{0}".format(fileend))

    return

def scan(filebase, *args, **kwargs):
    """Scan a range of voltages and make necessary characterization
    measurements.
    """
    
    ## Get first tuple of arguments and assign
    v_settings = args[0]
    v_name = v_settings[0]
    v_min = v_settings[1]
    v_max = v_settings[2]
    
    try:
        v_step = v_settings[3]
    except IndexError:
        v_step = 0.5

    fileend = kwargs.get("fileend", "")


    ## Set up loop for the voltage
    volts = v_min
    
    while (volts < v_max):

        voltage.set_voltage(volts, v_name)

        fileend2 = "{0}_{1}{2}".format(fileend, v_name, volts)

        ## If voltages remain, run again with remaining sets of parameters
        if len(args) > 1:

            kwargs.update({"fileend" : fileend2})
            scan(filebase, *args[1:], **kwargs)

        ## If list is exhausted perform measurement and increment
        else:
            sleep(1.0)

            ## Determine measurements to make
            imcount = kwargs.get("imcount")
            dtime = kwargs.get("dtime")
            all_stack(dtime, imcount, filebase, fileend2)

        ## Once all recursive voltage changes are made, increment
        volts += v_step

    return

###############################################################################
##
##  Single Frame
##
###############################################################################

def im_acq(mode, filename = "test.fits", time=0.00):
    """Perform an image exposure"""

    ## Delete output file, if it already exists
    try:
        os.remove(filename)
    except OSError as er:
        if er.errno != errno.ENOENT:
            raise

    ## Do exposure depending on specified mode
    if mode == "bias":
        output = subprocess.check_output(["dark_acq", "0.00",
                                          "{0}".format(filename)])
    elif mode == "dark":
        output = subprocess.check_output(["dark_acq", "{0}".format(time),
                                          "{0}".format(filename)])
    elif mode == "exp":
        output = subprocess.check_output(["exp_acq", "{0}".format(time),
                                          "{0}".format(filename)])

    return
                                        
        
def bias_acq(file_name='bias.fits'):
    """Acquire a bias frame"""

    ## Delete output file, if it exists
    try:
        os.remove(file_name)
    except OSError as er:
        if er.errno != errno.ENOENT:
            raise
        pass

    ## Do dark frame with 0.0 exposure time
    dark_acq(0.00, file_name)

def dark_acq(time, file_name=None):
    """Acquire a dark frame"""
    return  # Remove to allow measurement

    if filename is None:
        output = subprocess.check_output(["dark_acq", "{0}".format(time)])
    else:
        output = subprocess.check_output(["dark_acq", "{0}".format(time),
                                          "{0}".format(file_name)])
    return output

def exp_acq(exptime, filename=None):
    """Acquire and exposure image"""
    return # Remove to allow measurement

    if filename is None:
        output = subprocess.check_output(["exp_acq", "{0}".format(exptime)])
    else:
        output = subprocess.check_output(["exp_acq", "{0}".format(exptime),
                                          "{0}".format(file_name)])
    return output

def display(filename):

    output = subprocess.check_output(["ds9", "-mosaicimage", "iraf", 
                                      "{0}".format(filename), "-zoom",
                                      "to", "fit"])

    return output

###############################################################################
##
##  Stacks
##
###############################################################################

def bias_stack(imcount, filebase):
    """Collect a stack of bias frames"""

    i = 0

    while i < imcount: # Check if equality is allowed
        filename = "{0}_{1}.fits".format(filebase, i)
        print filename
        bias_acq(filename)
        i += 1

    return

def dark_stack(dtime, imcount, filebase, start=0):

    total = start + imcount

    i = start

    while i < total: # Check if equality is allowed
        filename = "{0}_{1}.fits".format(filebase, i)
        print filename
        dark_acq(dtime, filename)
        i += 1

    return

###############################################################################
##
##  Scans
##
###############################################################################

def old_bias_scan(imcount=4, od_min=25, od_max=30, od_step=0.5,
              rd_min=16, rd_max=20, rd_step=0.5):
    """Sweep through DR and RD voltages taking bias frames"""

    od_volts = od_min

    ## Outer loop cycles through OD voltages
    while (od_volts <= od_max):
        voltage.set_voltage(od_volts, "vod")
        rd_volts = rd_min

        ## At each OD voltage cycle through all RD voltages
        while (rd_volts <= rd_max):
            voltage.set_voltage(rd_volts, "vrd")
            sleep(1.0)
            filebase = "bias_OD{0:.1f}_RD{1:.1f}".format(od_volts, rd_volts)
            bias_stack(imcount, filebase)
            rd_volts += rd_step

        od_volts += od_step

    return

def bias_scan(imcount=4, od_min=25, od_max=30, od_step=0.5,
                  rd_min=16, rd_max=20, rd_step=0.5):

    vlist = [("vod", od_min, od_max, od_step),
             ("vrd", rd_min, rd_max, rd_step)]
    kwargs = {"imcount" : imcount}
    scan("Scan", *vlist, **kwargs)
        
def dark_scan(dtime, imcount, filebase, od_min=25, od_max=30,
              od_step=0.5, rd_min=16, rd_max=20, rd_step=0.5):

    od_volts = od_min

    while (od_volts < od_max):
        voltage.set_voltage(od_volts, "vod")
        rd_volts = rd_min

        while (rd_volts <= rd_max):
            voltage.set_voltage(rd_volts, "vrd")
            sleep(1.0)
            filebase2 = "{0}_OD{1:.1f}_RD{2:.1f}_{3:5.2f}".format(filebase,
                                                                  od_volts,
                                                                  rd_volts,
                                                                  dtime)

            dark_stack(dtime, imcount, filebase2)
            rd_volts += rd_step

        od_volts += od_step

    return

###############################################################################
##
##  Debug Code
##
###############################################################################

if __name__ == '__main__':

    ## Debug code

    ## This is example code to show how the scan code works
    #test_vlist = [("vod", 25, 26), ("vrd", 16, 17)]
    #dtime = 10
    #imcount = 15
    #kwargs = {"dtime" : 10, "imcount" : 2}
    #scan("test", *test_vlist, **kwargs)
    bias_scan()
    pass
