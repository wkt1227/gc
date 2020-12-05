import numpy as np


if __name__ == "__main__":
    comp_table = np.load('../data/result/comp_table.npy')
    tp, fp, tn, fn = 0.0, 0.0, 0.0, 0.0

    for r in comp_table:
        if r[0] > r[1]:
            tp += r[0]
            fp += r[1]
        else:
            tn += r[1]
            fn += r[0]

    recall = tp/(tp + fn)
    ftr = fp/(tn + fp)
    tss = recall - ftr
    
    tp, fp, tn, fn = map(int, [tp, fp, tn, fn])
    print('TP={}, FP={}, TN={}, FN={}'.format(tp, fp, tn, fn))
    print('再現率:{:.3}'.format(recall))
    print('偽陽性率:{:.3}'.format(ftr))
    print('TSS:{:.3}'.format(tss))