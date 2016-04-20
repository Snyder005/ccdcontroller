import fitsio
import os
import sys

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

    print filename

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

if __name__ == '__main__':

    update_header(str(sys.argv[1]))
    

    
