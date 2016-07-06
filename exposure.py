#!/usr/bin/env python

"""
This is a Python script to make different exposure measurements
"""

import subprocess
import os
import errno
from time import sleep

import voltage

## Import astropy.io.fits or pyfits
try:
    from astropy.io import fits
except ImportError:
    import pyfits as fits

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
            error = subprocess.CalledProcessError(retcode,cmd)
            error.output = output
            raise error
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

def im_acq(mode, filebase="test", exptime=0.00, seqnum=1, **kwargs):

    # If bias frame, set exptime to 0.00s
    if mode == "bias":
        exptime = 0.00
    
    filename = "{0}.{1}.{2}s.{3}.fits".format(filebase, mode,
                                             exptime, seqnum)

    ## Check that file doesn't exist already
    if os.path.isfile(filename):
        raise IOError

    ## Do exposure depending on specified mode
    if mode == "exp":
        output = subprocess.check_output(["exp_acq", "{0}".format(exptime),
                                          "{0}".format(filename)])
    elif mode in ['bias', 'dark']:
        output = subprocess.check_output(["exp_acq", "{0}".format(exptime),
                                          "{0}".format(filename)])

    ## Update FITs header
    update_header(filename, mode, exptime, seqnum, **kwargs)
    return filename

###############################################################################
##
##  FITs File Header Management
##
###############################################################################

def update_header(filepath, mode, exptime, seqnum, **kwargs):

    ## Exposure dependent kwargs
    filename = filepath
    if mode in ['bias', 'dark']:
        testtype = 'dark'
    elif mode == "exp":
        testtype = 'obs'
    imgtype = mode.upper()
    seqnum = seqnum
    temp_set = kwargs.get('temp_set', -95.00) ## Implement in later versions
    ccdtemp = kwargs.get('ccdtemp', -95.00) ## Implement in later versions
    mondiode = kwargs.get('mondiode', 143.12) ## Implement in later versions
    exptime = exptime

    ## Filter and monowl are mutually exclusive
    if 'monowl' in kwargs:
        monowl = kwargs.get('monowl')
        filter_name = 'N/A'
    elif 'filter_name' in kwargs:
        monowl = 'N/A'
        filter_name = kwargs.get('filter_name')
    else:
        monowl = 'N/A'
        filter_name = 'N/A'

    ## Settings from INI file
    imagetag = kwargs.get('imagetag', '[lots of digits]') ## Need to change
    tstand = kwargs.get('tstand', 'Stanford-KGLab')
    instrument = kwargs.get('instrument', 'SAO16')
    controller = kwargs.get('controller', 'SAO16')
    contnum = kwargs.get('contnum', 1)
    ccd_manu = kwargs.get('ccd_manu', 'ITL')
    ccd_type = kwargs.get('ccd_type', '3800C')
    ccd_sern = kwargs.get('ccd_sern', '19351')
    lsst_num = kwargs.get('lsst_num', '3800C-033')
    shut_del = kwargs.get('shut_del', 0.00)
    ctrlcfg = kwargs.get('ctrlcfg', 'abcde.xml') ## Need to look up
    binx = kwargs.get('binx', 1)
    biny = kwargs.get('biny', 1)
    headver = kwargs.get('headver', 1)
    ccdgain = kwargs.get('ccdgain', 5.52) ## Need to change
    ccdnoise = kwargs.get('ccdnoise', 6.0) ## Need to change

    ## Construct ccd conditions extensions.  Requires astropy python package
    ccdhdr = fits.Header()

    for i in range(16):
        ccdhdr['V_OD{0}'.format(i+1)] = kwargs.get('VOD', 0.0)
        ccdhdr['V_OG{0}'.format(i+1)] = kwargs.get('VOG', 0.0)
        ccdhdr['V_RD{0}'.format(i+1)] = kwargs.get('VRD', 0.0)

        if i <= 3:
            ccdhdr['V_S{0}L'.format(i+1)] = kwargs.get('SER LO', 0.0)
            ccdhdr['V_S{0}H'.format(i+1)] = kwargs.get('SER HI', 0.0)
            ccdhdr['V_P{0}L'.format(i+1)] = kwargs.get('PAR LO', 0.0)
            ccdhdr['V_P{0}H'.format(i+1)] = kwargs.get('PAR HI', 0.0)
                   
    ccdhdr['V_GD'] = kwargs.get('VGD', '') ## What is this? VDD?
    ccdhdr['V_BSS'] = kwargs.get('VBB', 0.0)
    ccdhdr['V_RGL'] = kwargs.get('RG LO', 0.0)
    ccdhdr['V_RGH'] = kwargs.get('RG HI', 0.0)
    
    ccdhdu = fits.ImageHDU(data=None, header=ccdhdr, name='CCD_COND')
    ccdhdu.add_checksum()

    ## Update fits header
    hdulist = fits.open(filepath, mode='update')
    prihdr = hdulist[0].header
    prihdr['IMAGETAG'] = (imagetag, 'Image tag (CCS/VST)')
    prihdr['TSTAND'] = (tstand, 'Test stand used.')
    prihdr['INSTRUME'] = (instrument, 'CCD Controller type')
    prihdr['CONTROLL'] = (controller, 'Duplicates INSTRUME')
    prihdr['CONTNUM'] = (contnum, 'CCD Controller Serial Number')
    prihdr['CCD_MANU'] = (ccd_manu, 'CCD Manufacturer')
    prihdr['CCD_TYPE'] = (ccd_type, 'CCD Model Number')
    prihdr['CCD_SERN'] = (ccd_sern, "Manufacturers' CCD Serial Number")
    prihdr['LSST_NUM']= (lsst_num, 'LSST Assigned CCD Number')
    prihdr['TESTTYPE'] = (testtype, 'dark:fe55:flat:lambda:spot:sflat_nnn:trap')
    prihdr['IMGTYPE'] = (imgtype, 'BIAS, DARK, ...')
    prihdr['SEQNUM'] = (seqnum, 'Sequence number')
    prihdr['TEMP_SET'] = (temp_set, 'Temperature set point')
    prihdr['CCDTEMP'] = (ccdtemp, 'Measured temperature')
    prihdr['MONDIODE'] = (mondiode, 'Current in monitoring diode')
    prihdr['MONOWL'] = (monowl, 'Monochromator wavelength')
    prihdr['FILTER'] = (filter_name, 'Name of the filter')
    prihdr['EXPTIME'] = (exptime, 'Exposure Time in Seconds')
    prihdr['SHUT_DEL'] = (shut_del, 'Shutter delay')
    prihdr['CTRLCFG'] = (ctrlcfg, 'CCD controller configuration file')
    prihdr['FILENAME'] = (os.path.split(filename)[1], 'Original name of the file')
    prihdr['BINX'] = (binx, '[pixels] binning along X axis')
    prihdr['BINY'] = (biny, '[pixels] binning along Y axis')
    prihdr['HEADVER'] = (headver, 'Version number of header')
    prihdr['CCDGAIN'] = (ccdgain, 'Rough guess at overall system gain')
    prihdr['CCDNOISE'] = (ccdnoise, 'Rough guess at system noise')

    hdulist.append(ccdhdu)
    hdulist.flush()
    hdulist.close()

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
