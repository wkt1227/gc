import numpy as np


if __name__ == "__main__":
    comp_table = np.load('../data/result/comp_table.npy')
    tp, fp, tn, fn = 0.0, 0.0, 0.0, 0.0

    for r in comp_table:
        if (r[0] > r[1]):
            tp += r[0]
            fp += r[1]
        else:
            tn = r[1]
            fn = r[0]

    recall = tp/(tp + fn)
    ftr = fp/(tn + fp)
    tss = recall - ftr

    print('再現率:{}'.format(recall))
    print('偽陽性率:{}'.format(ftr))
    print('TSS:{}'.format(tss))