import numpy as np
import glob
from astropy.modeling import models, fitting
import cv2
from libs.funcs import get_psd1d, get_psd2d


def gaussian_fitting(img):
    f_max, f_min, n_bin = 3000, 0, 3000
    x = np.linspace(f_min, f_max, n_bin + 1) + (f_max - f_min) / n_bin / 2
    x = x[:-1]
    pdf_fitted = np.histogram(img.flatten(), bins=n_bin, range=(f_min, f_max))
    pdf_fitted = pdf_fitted[0]
    fit = fitting.LevMarLSQFitter()
    gauss_init = models.Gaussian1D(mean=x[np.argmax(pdf_fitted)], stddev=100, amplitude=max(pdf_fitted))
    result = fit(gauss_init, x, pdf_fitted)
    
    return result.mean[0], result.stddev[0]


if __name__ == "__main__":
    npy_paths = glob.glob('../data/galaxy-npy/*')
    patch_features = []
    picked_pix_vals = []
    patch_labels = []
    label_cursor = 0

    for path in npy_paths:
        # npy読み込み
        img = np.load(path)


        # ccl
        mean, stddev = gaussian_fitting(img)
        img_p = img - mean

        img_b = cv2.threshold(img_p, 4*stddev, 255, cv2.THRESH_BINARY)[1]
        print(img_p, type(img_b))
        img_b = img_b.astype('uint8')
        retval, labels = cv2.connectedComponents(img_b)
        ctr_obj_label = labels[50, 50]
        picked_crds = np.array(np.where(labels == ctr_obj_label)).T

        
        # patch切り出し
        patch_size = 6
        for x, y in picked_crds:
            patch = img[x - patch_size:x + patch_size, y - patch_size:y + patch_size]
            # フーリエ変換->sample vector生成
            patch_feature = get_psd1d(get_psd2d(patch))  # radially average
            patch_features.append(patch_feature)
            picked_pix_vals.append(img[x, y])
            patch_labels.append(label_cursor)

        label_cursor += 1

    # 正規化（要素ごと）
    patch_features = np.array(patch_features)
    patch_features = (patch_features - patch_features.mean(axis=0)) /  patch_features.std(axis=0)

    np.save('../data/result/patch_features', patch_features)
    np.save('../data/result/patch_labels', patch_labels)
    
    # 銀河の明るさ、大きさを計算する
    galaxy_num = int(max(patch_labels)) + 1
    galaxy_sizes = np.zeros(galaxy_num)
    galaxy_brightnesses = np.zeros(galaxy_num)

    picked_pix_vals = np.array(picked_pix_vals)
    patch_labels = np.array(patch_labels).astype(np.int64)

    for i in range(galaxy_num):
        pts = np.where(patch_labels == i)

        galaxy_sizes[i] = len(pts[0])
        galaxy_brightnesses[i] = picked_pix_vals[pts].sum() / galaxy_sizes[i]

    np.save('../data/result/galaxy_sizes', galaxy_sizes)
    np.save('../data/result/galaxy_brightnesses', galaxy_brightnesses)