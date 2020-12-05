import numpy as np
import glob
from libs.funcs import get_psd1d, get_psd2d, get_zernikemoments_from_img


if __name__ == "__main__":
    spiral_paths = glob.glob('../data/galaxy-patch/SPIRAL/*')
    elliptical_paths = glob.glob('../data/galaxy-patch/ELLIPTICAL/*')
    label_cursor = 0
    patch_features = []
    patch_labels = []
    galaxy_brigtnesses = []
    galaxy_sizes = []
    galaxy_num = 1000
    
    for path in spiral_paths[:galaxy_num] + elliptical_paths[:galaxy_num]:
        patches = np.load(path)
        patch_size = patches[0].shape[0]
        galaxy_size = len(patches)
        galaxy_brigtness = 0

        for patch in patches:
            patch_feature = get_psd1d(get_psd2d(patch)) # radially average
            # patch_feature = get_psd2d(patch).flatten() # radially average を取らない
            zernikemoments = get_zernikemoments_from_img(patch)  # zernike moments
            patch_feature = np.append(patch_feature, zernikemoments)
            patch_features.append(patch_feature)
            patch_labels.append(label_cursor)
            galaxy_brigtness += patch[patch_size//2, patch_size//2] 

        galaxy_brigtness /= galaxy_size
        galaxy_brigtnesses.append(galaxy_brigtness)
        galaxy_sizes.append(galaxy_size)
        label_cursor += 1

    # 正規化
    patch_features = np.array(patch_features)
    patch_features = (patch_features - patch_features.mean(axis=0)) / patch_features.std(axis=0)
    # 正規化（ベクトルごと）
    # patch_features = np.array(patch_features)
    # patch_features = (patch_features - patch_features.mean(axis=1, keepdims=True)) / patch_features.std(axis=1, keepdims=True)
    # 割合にする
    # patch_features = np.array(patch_features)
    # s = patch_features.sum(axis=1, keepdims=True)
    # patch_features /= s

    np.save('../data/result/patch_features', patch_features)
    np.save('../data/result/patch_labels', patch_labels)
    np.save('../data/result/galaxy_labels_in_gz', ['SPIRAL']*galaxy_num + ['ELLIPTICAL']*galaxy_num)
    np.save('../data/result/galaxy_sizes', galaxy_sizes)
    np.save('../data/result/galaxy_brightnesses', galaxy_brigtnesses)