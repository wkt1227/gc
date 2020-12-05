import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

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

    p = mp.Pool(mp.cpu_count())
    inputs = [(v, gng_output) for v in gng_input]
    patch_labels2 = hc_result[p.map(f, inputs)]
    p.close()

    np.save('../data/result/patch_labels2.npy', patch_labels2)

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(gng_output[:, 0], gng_output[:, 1], gng_output[:, 2], c=np.array(hc_result), s=50, zorder=1, alpha=0.2, cmap=cm.hsv)
    sc = ax.scatter(gng_input[:, 0], gng_input[:, 1], gng_input[:, 2], c=np.array(patch_labels2), s=2, zorder=2, cmap=cm.hsv)
    plt.colorbar(sc)
    plt.savefig('../reports/gng_hc_clustering')
    plt.close()