import fitsio
import os
import sys
import numpy as np

def update_header(filepath, **kwargs):

    fits = fitsio.FITS(filepath, 'rw')

    img = np.zeros((0,0))
    
    hdict = {'V_OD' : 15.0,
             'V_RD' : 15.0}

    fits.write(img, hdict)

if __name__ == '__main__':

    update_header(str(sys.argv[1]))
    

    
