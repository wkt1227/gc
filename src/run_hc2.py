# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, fcluster, centroid, single, complete, average, weighted, median, ward
from scipy.spatial.distance import pdist


if __name__ == "__main__":
    galaxy_vectors = np.load('../data/result/galaxy_vectors.npy')

    Z = centroid(pdist(galaxy_vectors, 'correlation'))
    maxclust = 50
    ct = Z[-(maxclust-1), 2]
    cl = fcluster(Z, maxclust, criterion='maxclust')
    plt.axhline(ct, linestyle='--', c='purple')
    dendrogram(Z, color_threshold=ct, labels=cl)
    plt.title('cluster:{}'.format(cl.max()))
    plt.savefig('../reports/hc2_result')
    plt.close()

    np.save('../data/result/galaxy_labels', cl)