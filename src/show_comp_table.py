import numpy as np


if __name__ == "__main__":
    comp_table = np.load('../data/result/comp_table.npy')

    print(' cl   sp   el  size ave.  brightness ave.')
    print('-----------------------------------------')
    for i, r in enumerate(comp_table):
        sp, el, size, brightness = r
        print('{:3} [{:3}, {:3}] {:>9.1f}  {:>9.1f}'.format(i+1, int(sp), int(el), size, brightness))