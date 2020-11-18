import numpy as np
import multiprocessing as mp

def f(args):
    v, gng_output = args
    nearest_idx = 0
    dist = 0

    for j, u in enumerate(gng_output):
        tmp_dist = np.linalg.norm(v-u)

        if j == 0:
            dist = tmp_dist
            continue

        if tmp_dist < dist:
            dist = tmp_dist
            nearest_idx = j

    return nearest_idx

if __name__ == "__main__":
    
    gng_input = np.load('../data/result/patch_features.npy')
    gng_output = np.load('../data/result/gng_result.npy')
    hc_result = np.load('../data/result/hc_result.npy')

    p = mp.Pool(3)
    inputs = [(v, gng_output) for v in gng_input]
    patch_labels2 = hc_result[p.map(f, inputs)]
    p.close()

    np.save('../data/result/patch_labels2.npy', patch_labels2)