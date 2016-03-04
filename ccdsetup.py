#!/usr/bin/env python

"""
This is a Python script for automation of the characterization of an ITL CCD 
by changing voltages.
"""

import sys
import argparse
import subprocess

import voltage
import exposure

from time import sleep
from Phidgets.Devices.InterfaceKit import InterfaceKit

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
##  Miscellaneous Functions
##
###############################################################################


###############################################################################
##
##  Configuration Parameters
##
###############################################################################

def par_speed(speed):
    """Set parallel clock speed"""

    output = subprocess.check_output(["par_speed", "{0}".format(speed)])
    print output
    return output
    
def patload(pat_file):
    """Convert and load a pattern file"""
    
    output = subprocess.check_output(["patload", "{0}".format(pat_file)])
    print output
    return output

def sigload(sig_file):
    """Convert and load a signal file"""

    output = subprocess.check_output(["sigload", "{0}".format(sig_file)])
    print output
    return output

def set_bbias(state):
    """Set back bias to state"""

    state_dict = {"On" : True,
                  "Off" : False}
    setting = state_dict[state]

    ## Attach to Phidget controller
    relay = InterfaceKit()
    relay.openPhidget()
    relay.waitForAttach(10000)

    ## Check if successful
    if relay.isAttached():
        print "Done!"
    else:
        print "Failed to connect to Phidget controller"

    ## Set output to 0 and close
    relay.setOutputState(0, setting)
    print "BSS is now {0}".format(state)
    relay.closePhidget()

    return

def offset(chan, val):
    """Set channel to specified value"""
    
    output = subprocess.check_output(["offset", "{0}".chan, "{0}".value])
    print output
    return output

def seg_offset(seg, val):
    """Set segment channel to specified value"""

    chan_dict = { 1 :  1,
                  2 :  5,
                  3 :  2,
                  4 :  6,
                  5 :  3,
                  6 :  7,
                  7 :  4,
                  8 :  8,
                  9 :  9,
                 10 : 13,
                 11 : 10,
                 12 : 14,
                 13 : 11,
                 14 : 15,
                 15 : 12,
                 16 : 16}

    chan = chan_dict[seg]
    offset(chan, val)

    return

## Ignore for now, not used
def bbs(num):
    pass

###############################################################################
##
##  Main Set-up Functions
##
###############################################################################

def ch_setup():
    """Set up for generic 16 channel readout"""

    output = subprocess.check_output("16ch_setup")
    print output
    return output

def sta3800_timing():
    """Set the default CCD readout timing for the STA3800 device"""

    par_speed(6)

    sigload("sta3800a.sig")

    patload("sta3800a.pat")
  
    return

def sta3800_channels():
    """Set up for 16 channel readout"""
    
    output = subprocess.check_output("sta3800_channels")
    print output
    return output

def sta3800_volts():
    """Set the default voltages for the STA3800 device"""

    voltage.v_clk(0.0, 10.0)

    ## For use with Kirk's switch BBS supply
    sleep(0.5)
    set_bbias("Off")
    # bss(0.0) # For use with separate BSS supply

    ## Set VDD
    voltage.set_voltage(19.0, "vdd")
    sleep(0.5)

    ## Set VRD
    voltage.set_voltage(13.0, "vrd")
    sleep(0.5)
    
    ## Set VOD
    voltage.set_voltage(25.00, "vod")
    sleep(0.5)

    ## Set VOG
    voltage.set_voltage(0.0, "vog")
    sleep(0.5)

    ## Set clocks
    voltage.par_clks(-8.00, 4.00)
    voltage.ser_clks(-4.00, 6.00)
    voltage.rg(-2.00, 8.00)
    sleep(0.5)

    ## For use with Kirk's switch BBS suply
    set_bbias("On")
    # bss(0.0) # For use with separate BSS supply

    return

def sta3800_offset():
    """Set ADC channel offsets for STA3800 CCD"""

    setting_list = [4008, 3488, 3209, 4031, 4008, 4007, 3600, 136,
                    3993, 2703, 4002, 4012, 84, 4000, 3765, 4043]

    for i in range(16):
        seg_offset(i+1, setting_list[i])

    return

def gain(mode):
    """Set the gain of the SAO controller to either high or low mode"""

    output = subprocess.check_output(["gain", "{0}".format(mode)])
    print output
    return output
    

def sta3800_setup(use_bash=True):

    if use_bash:
        print "Turning on the sta3800 system."
        output = subprocess.check_output("sta3800_setup")
        print output
        return

    ch_setup()

    sta3800_timing()
    sta3800_channels()
    sta3800_volts()
    sta3800_offset()
    gain("high")

def sta3800_off(use_bash=True):

    if use_bash:
        print "Turning off the sta3800 system."
        output = subprocess.check_output("sta3800_off")
        print output
        return


###############################################################################
##
##  Main Function and Argument Parser
##
###############################################################################

def main():

    sta3800_setup(use_bash=False)

    return

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Automate ITL CCD characterization",
                                     prog='CCD Autochar')
    parser.add_argument("-c", "--config", default=None, metavar='',
                        help="Specify config filepath")
    parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.1')
    args = parser.parse_args()

    main()
