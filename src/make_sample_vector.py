import numpy as np
import glob
from libs.funcs import get_psd1d, get_psd2d


if __name__ == "__main__":
    spiral_paths = glob.glob('../data/galaxy-patch/SPIRAL/*')
    elliptical_paths = glob.glob('../data/galaxy-patch/ELLIPTICAL/*')
    label_cursor = 0
    patch_features = []
    patch_labels = []
    galaxy_num = 1000
    
    for path in spiral_paths[:galaxy_num] + elliptical_paths[:galaxy_num]:
        patches = np.load(path)

        for patch in patches:
            # patch_feature = get_psd1d(get_psd2d(patch)) # radially average
            patch_feature = get_psd2d(patch).flatten() # radially average を取らない
            patch_features.append(patch_feature)
            patch_labels.append(label_cursor)

        label_cursor += 1

    # 正規化
    patch_features = np.array(patch_features)
    patch_features = (patch_features - patch_features.mean(axis=0)) / patch_features.std(axis=0)

    np.save('../data/result/patch_features', patch_features)
    np.save('../data/result/patch_labels', patch_labels)
    np.save('../data/result/galaxy_labels_in_gz', ['SPIRAL']*galaxy_num + ['ELLIPTICAL']*galaxy_num)