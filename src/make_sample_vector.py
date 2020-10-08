import numpy as np
import glob


if __name__ == "__main__":
    npy_paths = glob.glob('../data/galaxy-npy/*')

    for path in npy_paths:
        # npy読み込み
        galaxy_arr = np.load(path)

        # CCL

        # patch切り出し

        # フーリエ変換->sample vector生成

        