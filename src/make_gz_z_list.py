# coding: utf-8
import numpy as np
import multiprocessing as mp
from libs.funcs import get_z_from_objid

if __name__ == "__main__":
    objid_list = np.load('../data/objid_list.npy')
    p = mp.Pool(mp.cpu_count())
    z_list = [p.map(get_z_from_objid, objid_list)]
    p.close()
    np.save('../data/z_list.npy', z_list)