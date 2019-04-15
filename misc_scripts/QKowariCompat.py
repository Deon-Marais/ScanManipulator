'''
Created on 05 Mar 2014

@author: Deon
'''

import h5py
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2 :
        print("Usage: " + sys.argv[0] + " <hdf filename>")
        sys.exit()
    filename = sys.argv[1]
    fin = h5py.File(filename,"a")
    dset = fin.get("/")
    try:
        dset.copy("entry1/instrument/run_number","entry1/data/run_number")
        print("Copied 'entry1/instrument/run_number' to 'entry1/data/run_number'\r\n")
    except Exception, e:
        print("'entry1/instrument/run_number' not copied to 'entry1/data/run_number', " + e.message)
    hmm = dset['entry1/data/hmm']
    msg = "Changed hmm axes property from '" +  hmm.attrs["axes"] + "' to '"
    hmm.attrs["axes"] = "run_number:" + hmm.attrs["axes"].split(":",1)[1]
    msg += hmm.attrs["axes"] + "'"
    print(msg)
    fin.close()
    
    pass
