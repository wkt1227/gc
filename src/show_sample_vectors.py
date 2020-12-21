import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

patch_features = np.load('../data/result/patch_features.npy')
patch_morph_labels = np.load('../data/result/patch_morph_labels.npy')
cdict = {'SPIRAL': 'red', 'ELLIPTICAL': 'blue'}
c = [cdict[x] for x in patch_morph_labels]

sp = len(np.where(patch_morph_labels == 'SPIRAL')[0])
el = len(np.where(patch_morph_labels == 'ELLIPTICAL')[0])
print(f'sp:{sp}, el:{el}')

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(patch_features[:, 0], patch_features[:, 1], patch_features[:, 2], s=1, alpha=0.2, c=c)

plt.title(f'sample vectors: {len(patch_features)}')
ax.set_xlabel('sample vector[0]')
ax.set_ylabel('sample vector[1]')
ax.set_zlabel('sample vector[2]')
ax.legend()
plt.savefig(f'../reports/sp:{sp}, el:{el}')