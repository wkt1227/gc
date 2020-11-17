import numpy as np


if __name__ == "__main__":
    comp_table = np.load('../data/result/comp_table.npy')

    print(' cl   sp   el')
    print('--------------')
    for i, r in enumerate(comp_table):
        sp, el = r
        print('{:3} [{:3}, {:3}]'.format(i+1, int(sp), int(el)))