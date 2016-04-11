#!/usr/bin/env python

"""
This is a Python script to make different exposure measurements
"""

import subprocess
import os
import errno

import voltage

from time import sleep

## For Python 2.6 need to monkey patch in check_output()
if "check_output" not in dir( subprocess ):
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
##  Voltage Scans - For Future Use
##
###############################################################################

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
##  Exposures
##
###############################################################################

def im_acq(mode, filebase="test", time=0.00):
    """Perform an image exposure of given mode."""

    filename = "{0}.fits".format(filebase)

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

    return filename

def stack(mode, filebase, imcount, time, start=0):
    """Perform a stack of images of a given mode."""

    total = start + imcount

    i = start

    while i < total:

        filename = "{0}.{1}".format(filebase, i)
        im_acq(mode, filename, time)
        i += 1

    return

def series(mode, filebase, mintime, maxtime, step):
    """Perform a series of images of a given mode."""

    time = mintime

    while time <= maxtime:
        filename = "{0}.{1}s".format(filebase, time)
        im_acq(mode, filename, time)
        dtime += step

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
