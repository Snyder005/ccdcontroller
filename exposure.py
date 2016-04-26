#!/usr/bin/env python

"""
This is a Python script to make different exposure measurements
"""

import subprocess
import os
import errno
import fitsio

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

    ## If output file already exists raise an error
    if os.path.isfile(filename):
        raise IOError

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

    ## Update header
    update_header(filename, testtype=mode.upper(), imgtype=mode.upper(), exptime=time)
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
##  FITs File Header Management
##
###############################################################################

def update_header(filepath, **kwargs):

    ## Get header items from kwargs dictionary
    imagetag = kwargs.pop('imagetag', '[lots of digits]')
    tstand = kwargs.pop('tstand', 'BNL1')
    instrument = kwargs.pop('instrument', 'SAO4')
    controller = kwargs.pop('controller', 'SAO4')
    contnum = kwargs.pop('contnum', 3)
    ccd_manu = kwargs.pop('ccd_manu', 'ITL')
    ccd_type = kwargs.pop('ccd_type', '3800C')
    ccd_sern = kwargs.pop('ccd_sern', '19351') 
    lsst_num = kwargs.pop('lsst_num', '3800C-033')
    testtype = kwargs.pop('testtype', 'FLAT')
    imgtype = kwargs.pop('imgtype', 'FLAT')
    seqnum = kwargs.pop('seqnum', 123)
    temp_set = kwargs.pop('temp_set', -95.00)
    ccdtemp = kwargs.pop('ccdtemp', -95.12)
    mondiode = kwargs.pop('mondiode', 143.12)
    monowl = kwargs.pop('monowl', 550.00)
    filter_name = kwargs.pop('filter_name', '550LP')
    exptime = kwargs.pop('exptime', 10.00)
    shut_del = kwargs.pop('shut_del', 100.00)
    ctrlcfg = kwargs.pop('ctrlcfg', 'abcde.xml')
    filename = kwargs.pop('filename', os.path.basename(filepath))
    binx = kwargs.pop('binx', 1)
    biny = kwargs.pop('biny', 1)
    headver = kwargs.pop('headver', 1)
    ccdgain = kwargs.pop('ccdgain', 5.52)
    ccdnoise = kwargs.pop('ccdnoise', 6.0)

    ## Update fits header
    fits = fitsio.FITS(filepath, 'rw')
    fits[0].write_key('IMAGETAG', imagetag, comment='Image tag (CCS/VST)')
    fits[0].write_key('TSTAND', tstand, comment = 'Which test stand at the site was used.')
    fits[0].write_key('INSTRUME', instrument, comment='CCD Controller type')
    fits[0].write_key('CONTROLL', controller, comment='Duplicates INSTRUME')
    fits[0].write_key('CONTNUM', contnum, comment='CCD Controller Serial Number')
    fits[0].write_key('CCD_MANU', ccd_manu, comment='CCD Manufacturer')
    fits[0].write_key('CCD_TYPE', ccd_type, comment='CCD Model Number')
    fits[0].write_key('CCD_SERN', ccd_sern, comment="Manufacturers' CCD Serial Number")
    fits[0].write_key('LSST_NUM', lsst_num, comment='LSST Assigned CCD Number')
    fits[0].write_key('TESTTYPE', testtype, comment='dark:fe55:flat:lambda:spot:sflat_nnn:trap')
    fits[0].write_key('IMGTYPE', imgtype, comment='BIAS, DARK, ...')
    fits[0].write_key('SEQNUM', seqnum, comment='Sequence number extracted from the original filename')
    fits[0].write_key('TEMP_SET', temp_set, comment='Temperature set point')
    fits[0].write_key('CCDTEMP', ccdtemp, comment='Measured temperature')
    fits[0].write_key('MONDIODE', mondiode, comment='Current in the monitoring diode')
    fits[0].write_key('MONOWL', monowl, comment='Monochromator wavelength')
    fits[0].write_key('FILTER', filter_name, comment='Name of the filter')
    fits[0].write_key('EXPTIME', exptime, comment='Exposure Time in Seconds')
    fits[0].write_key('SHUT_DEL', shut_del, comment='Delay between shutter close command and readout')
    fits[0].write_key('CTRLCFG', ctrlcfg, comment='Name of the CCD controller configuration file')
    fits[0].write_key('FILENAME', filename, comment='Original name of the file')
    fits[0].write_key('BINX', binx, comment='[pixels] binning along X axis')
    fits[0].write_key('BINY', biny, comment='[pixels] binning along Y axis')
    fits[0].write_key('HEADVER', headver, comment='Version number of header')
    fits[0].write_key('CCDGAIN', ccdgain, comment='Rough guess at overall system gain')
    fits[0].write_key('CCDNOISE', ccdnoise, comment='Rough guess at system noise')
    fits.close()

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
