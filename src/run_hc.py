# coding: UTF-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.hierarchy import dendrogram, fcluster, centroid, ward
from scipy.spatial.distance import pdist


if __name__ == "__main__":
    
    gng_input = np.load('../data/result/patch_features.npy')
    gng_output = np.load('../data/result/gng_result.npy')

    # 階層的クラスタリング
    if sys.argv[1] == 'd':
        Z = centroid(pdist(gng_output, 'correlation'))
        ct = 0.045
        dendrogram(Z, color_threshold=ct)    
        cl = fcluster(Z, ct, criterion='distance')
    
    else:
        if sys.argv[1] == 'c':
            Z = centroid(pdist(gng_output, 'correlation'))
        else:
            Z = ward(pdist(gng_output, 'correlation'))

        maxclust = int(sys.argv[2])
        ct = Z[-(maxclust-1), 2]
        dendrogram(Z, color_threshold=ct)
        cl = fcluster(Z, maxclust, criterion='maxclust')

    plt.axhline(ct, linestyle='--', c='purple')
    plt.title('cluster:{}'.format(cl.max()))
    plt.savefig('../reports/hc_result')
    plt.close()


    np.save('../data/result/hc_result.npy', cl)