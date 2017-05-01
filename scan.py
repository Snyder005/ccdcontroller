import exposure
import numpy as np

## test for invalid voltage names and values

class Dummy():

    def scan(self, filename, data_dir, *vparams_list, **kwargs):
                

                   

################################

def scan_params(filename):

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
