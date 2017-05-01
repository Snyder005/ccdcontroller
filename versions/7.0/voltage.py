#!/usr/bin/env python

"""This is a Python module to control changing CCD control voltages


Currently bash scripts for voltage control are called, and output returned.
This will allow the easy ability to parse output to command line or GUI.
"""

import subprocess

## For Python 2.6 need to monkey patch check_output()
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
##  Voltage controls
##
###############################################################################

def v_clk(V_lo, V_hi):
    """Set limits for bbs switch"""
    
    output = subprocess.check_output(["v_clk", "{0}".format(V_lo),
                                      "{0}".format(V_hi)])
    return output

def set_voltage(V, vname):
    """Set a particular voltage to specified value"""

    ## List of acceptable voltage names
    if vname in ["VDD", "VOD", "VOG", "VRD"]:
        output = subprocess.check_output([vname.lower(), "{0}".format(V)])
        return output
    else:
        raise KeyError("Voltage name not found.")

def rg(rg_lo, rg_hi):
    """Set reset gate voltages"""
    
    output = subprocess.check_output(["rg", "{0}".format(rg_lo),
                                      "{0}".format(rg_hi)])
    return output

def par_clks(par_lo, par_hi):
    """Set parallel clock rails to specified voltages"""
    
    output = subprocess.check_output(["par_clks", "{0}".format(par_lo),
                                      "{0}".format(par_hi)])
    return output

def ser_clks(ser_lo, ser_hi):
    """Set parallel clock rails to specified voltages"""
    
    output = subprocess.check_output(["ser_clks", "{0}".format(ser_lo),
                                      "{0}".format(ser_hi)])
    return output

###############################################################################
##
##  Debug Function
##
###############################################################################

if __name__ == '__main__':

    ## Module debug code here
    set_voltage(15, "vrd")
    pass
