import numpy as np


if __name__ == "__main__":
    comp_table = np.load('../data/result/comp_table.npy')

    print(' cl   sp   el  size ave.  brightness ave.  z ave.')
    print('-------------------------------------------------')
    for i, r in enumerate(comp_table):
        sp, el, size, brightness, z = r
        print('{:3} [{:3}, {:3}] {:>9.1f}  {:>9.1f}  {:>12.3f}'.format(i+1, int(sp), int(el), size, brightness, z))