#!/usr/bin/env python

"""
This is a Python script to make different exposure measurements
"""

import subprocess
import os
import errno
from time import sleep
from time import time as timestamp
from datetime import datetime
import math
import pytz

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

    ## Set up loop for the voltage
    volts = v_min
    
    while (volts < v_max):

        voltage.set_voltage(volts, v_name)

        ## If voltages remain, run again with remaining sets of parameters
        if len(args) > 1:

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

    is_test = kwargs.get('is_test', True)

    # If bias frame, set exptime to 0.00s
    if mode == "bias":
        exptime = 0.00
    
    filename = "{0}.{1}.{2}s.{3}.fits".format(filebase, mode,
                                                  exptime, seqnum)

    ## Check that file doesn't exist already
    if not is_test:
        if os.path.isfile(filename):
            raise IOError

    ## Do exposure depending on specified mode
    if mode == "exp":
        output = subprocess.check_output(["exp_acq", "{0}".format(exptime),
                                          "{0}".format(filename)])
    elif mode in ['bias', 'dark']:
        output = subprocess.check_output(["dark_acq", "{0}".format(exptime),
                                          "{0}".format(filename)])

    ## Update FITs header
    update_header(filename, mode, exptime, seqnum, **kwargs)
    return filename

###############################################################################
##
##  FITs File Header Management
##
###############################################################################

def hmsm_to_days(hour=0,min=0,sec=0,micro=0):
    """
    Convert hours, minutes, seconds, and microseconds to fractional days.
    
    Parameters
    ----------
    hour : int, optional
        Hour number. Defaults to 0.
    
    min : int, optional
        Minute number. Defaults to 0.
    
    sec : int, optional
        Second number. Defaults to 0.
    
    micro : int, optional
        Microsecond number. Defaults to 0.
        
    Returns
    -------
    days : float
        Fractional days.
        
    Examples
    --------
    >>> hmsm_to_days(hour=6)
    0.25
    
    """
    days = sec + (micro / 1.e6)
    
    days = min + (days / 60.)
    
    days = hour + (days / 60.)
    
    return days / 24.

def date_to_jd(year,month,day):
    """
    Convert a date to Julian Day.
    
    Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet', 
        4th ed., Duffet-Smith and Zwart, 2011.
    
    Parameters
    ----------
    year : int
        Year as integer. Years preceding 1 A.D. should be 0 or negative.
        The year before 1 A.D. is 0, 10 B.C. is year -9.
        
    month : int
        Month as integer, Jan = 1, Feb. = 2, etc.
    
    day : float
        Day, may contain fractional part.
    
    Returns
    -------
    jd : float
        Julian Day
        
    Examples
    --------
    Convert 6 a.m., February 17, 1985 to Julian Day
    
    >>> date_to_jd(1985,2,17.25)
    2446113.75
    
    """
    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month
    
    # this checks where we are in relation to October 15, 1582, the beginning
    # of the Gregorian calendar.
    if ((year < 1582) or
        (year == 1582 and month < 10) or
        (year == 1582 and month == 10 and day < 15)):
        # before start of Gregorian calendar
        B = 0
    else:
        # after start of Gregorian calendar
        A = math.trunc(yearp / 100.)
        B = 2 - A + math.trunc(A / 4.)
        
    if yearp < 0:
        C = math.trunc((365.25 * yearp) - 0.75)
    else:
        C = math.trunc(365.25 * yearp)
        
    D = math.trunc(30.6001 * (monthp + 1))
    
    jd = B + C + D + day + 1720994.5
    
    return jd

def datetime_to_jd(date):
    """
    Convert a `datetime.datetime` object to Julian Day.
    
    Parameters
    ----------
    date : `datetime.datetime` instance
    
    Returns
    -------
    jd : float
        Julian day.
        
    Examples
    --------
    >>> d = datetime.datetime(1985,2,17,6)  
    >>> d
    datetime.datetime(1985, 2, 17, 6, 0)
    >>> jdutil.datetime_to_jd(d)
    2446113.75
    
    """
    days = date.day + hmsm_to_days(date.hour,date.minute,date.second,date.microsecond)
    
    return date_to_jd(date.year,date.month,days)

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
    imagetag = kwargs.get('imagetag', "{0}".format(int(timestamp()))) ## Need to change
    tstand = kwargs.get('tstand', 'Stanford-KGLab')
    instrument = kwargs.get('instrument', 'SAO16')
    controller = kwargs.get('controller', 'SAO16')
    contnum = kwargs.get('contnum', 1)
    ccd_manu = kwargs.get('ccd_manu', 'ITL')
    ccd_type = kwargs.get('ccd_type', '3800C')
    ccd_sern = kwargs.get('ccd_sern', '19351')
    lsst_num = kwargs.get('lsst_num', '3800C-033')
    shut_del = kwargs.get('shut_del', 0.00)
    ctrlcfg = kwargs.get('ctrlcfg', 'sta3800a.sig') ## Need to look up
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
    
    ## Add properly formated Date information to FITs header
    date_str = prihdr['DATE']
    dt = datetime.strptime(date_str, '%a %b %d %H:%M:%S %Z %Y')
    local = pytz.timezone('GMT')
    local_dt = local.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    utc_dt_obs = datetime.utcnow()

    date_utc = utc_dt.strftime('%Y-%m-%dT%H:%M:%S.000')
    date_mjd = datetime_to_jd(utc_dt)
    date_obs_utc = utc_dt_obs.strftime('%Y-%m-%dT%H:%M:%S.000')

    prihdr['DATE-OBS'] = (date_utc, 'Date of the observation')
    prihdr['DATE'] = (date_obs_utc, 'Creation Date and Time of File')
    prihdr['MJD'] = ('{0:.5f}'.format(date_mjd), 
                     'Modified Julian Date of image acquisition')

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
