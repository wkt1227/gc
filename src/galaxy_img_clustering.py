import shutil
import glob
import numpy as np
import re


if __name__ == "__main__":
    galaxy_labels = np.load('../data/result/galaxy_labels.npy')
    sp_img_paths = glob.glob('../data/galaxy-img/SPIRAL/*')
    el_img_paths = glob.glob('../data/galaxy-img/ELLIPTICAL/*')

    img_num = len(galaxy_labels) // 2
    img_paths = sp_img_paths[:img_num] + el_img_paths[:img_num]

    for label, path in zip(galaxy_labels, img_paths):
        galaxy_id = re.search(r'/(\d+).png', path).groups()[0]
        galaxy_type = re.search(r'/(\w+)/\d+.png', path).groups()[0]

        if galaxy_type == 'SPIRAL':
            galaxy_type = 'Sp'
        else:
            galaxy_type = 'El'

        dest = '../data/result/galaxycluster/' + str(label) + '/' + galaxy_id + '_' + galaxy_type + '.png'
        print(path)
        print(dest)

        shutil.copy(path, dest)