# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.hierarchy import dendrogram, fcluster, centroid
from scipy.spatial.distance import pdist


if __name__ == "__main__":
    
    gng_input = np.load('../data/result/patch_features.npy')
    gng_output = np.load('../data/result/gng_result.npy')

    # 階層的クラスタリング
    Z = centroid(pdist(gng_output, 'correlation'))
    # ct = 0.003
    ct = 0.045
    # ct = 0.35
    dendrogram(Z, color_threshold=ct)    
    cl = fcluster(Z, ct, criterion='distance')

    # maxclust = 231
    # ct = Z[-(maxclust-1), 2]
    # dendrogram(Z, color_threshold=ct)
    # cl = fcluster(Z, maxclust, criterion='maxclust')

    plt.axhline(ct, linestyle='--', c='purple')
    plt.title('cluster:{}'.format(cl.max()))
    plt.savefig('../reports/hc_result')
    plt.close()


    np.save('../data/result/hc_result.npy', cl)


    patch_labels2 = []

    for i, v in enumerate(gng_input):
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

        patch_labels2.append(cl[nearest_idx])

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(gng_output[:, 0], gng_output[:, 1], gng_output[:, 2], c=np.array(cl), s=50, zorder=1, alpha=0.2, cmap=cm.hsv)
    sc = ax.scatter(gng_input[:, 0], gng_input[:, 1], gng_input[:, 2], c=np.array(patch_labels2), s=2, zorder=2, cmap=cm.hsv)
    plt.colorbar(sc)
    plt.savefig('../reports/gng_hc_clustering')
    plt.close()

    np.save('../data/result/patch_labels2.npy', patch_labels2)