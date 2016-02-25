#!/usr/bin/env python

"""This is a Python module to control changing CCD control voltages


   Currently bash scripts for voltage control are called, and output returned.
   This will allow the easy ability to parse output to command line or GUI.
"""

import subprocess

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
##  Voltage controls
##
###############################################################################

def v_clk(V_lo, V_hi):
    """Set limits for bbs switch"""
    
    output = subprocess.check_output(["v_clk", "{0}".format(V_lo),
                                      "{0}".format(V_hi)])
    return output
    pass

def set_voltage(V, vname):
    """Set a particular voltage to specified value"""

    ## List of acceptable voltage names
    vlist = ["vdd", "vod", "vog", "vrd", "vv1", "vv2", "vv3", "vv4"]

    ## Check that voltage name is valid
    if vname in vlist:
        output = subprocess.check_output([vname, "{0}".format(V)])
        return output
    else:
        raise KeyError("Voltage name not found.")

def rg(RG_lo, RG_hi):
    """Set reset gate voltages"""
    
    output = subprocess.check_output(["rg", "{0}".format(RG_lo),
                                      "{0}".format(RG_hi)])
    return output

def par_clks(PAR_lo, PAR_hi):
    """Set parallel clock rails to specified voltages"""
    
    output = subprocess.check_output(["par_clks", "{0}".format(PAR_lo),
                                      "{0}".format(PAR_hi)])
    return output

def ser_clks(SER_lo, SER_hi):
    """Set parallel clock rails to specified voltages"""
    
    output = subprocess.check_output(["ser_clks", "{0}".format(SER_lo),
                                      "{0}".format(SER_hi)])
    return output

###############################################################################
##
##  Debug Function
##
###############################################################################

if __name__ == '__main__':

    ## Module debug code here
    output = set_voltage(15, "vrd")
    print output
    pass
