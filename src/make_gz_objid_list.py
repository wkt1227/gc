from astropy.table import Table
import numpy as np


gz_table = Table.read('../data/GalaxyZoo1_DR_table2.fits')
print(len(gz_table))
objid_list = []
for r in gz_table:
    objid = r[0]
    objid_list.append(objid)

print(len(objid_list))
np.save('../data/objid_list.npy', objid_list)