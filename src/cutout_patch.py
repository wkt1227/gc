import numpy as np
import glob
import matplotlib.pyplot as plt
import cv2

import astropy.io.fits as iofits
from astropy.modeling import models, fitting
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.table import Table


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

    fits_paths = glob.glob('/media/wkt1227/ec0839a8-1d89-4192-a30f-77387e2e2c04/data_rbands/*/*')
    gz_table = Table.read('../data/GalaxyZoo1_DR_table2.fits')
    galaxy_fits_name_in_gz = np.load('../data/galaxy_fits_name_in_gz.npy')
    galaxy_types = ['SPIRAL', 'ELLIPTICAL', 'UNCERTAIN']

    for path in fits_paths[:5000]:
        print(path)
        fits = iofits.open(path)
        img = fits[0].data
        header = fits[0].header
        wcs = WCS(header)

        mean, stddev = gaussian_fitting(img)
        img_p = img - mean

        # CCL
        img_b = cv2.threshold(img_p, 4*stddev, 255, cv2.THRESH_BINARY)[1]
        img_b = img_b.astype('uint8')
        retval, labels = cv2.connectedComponents(img_b)

        fits_name = path[-25:]
        idxs = np.where(galaxy_fits_name_in_gz == fits_name)
        for r in gz_table[idxs]:
            patches = []

            galaxy_id = r[0]
            ra_hms = r[1]
            dec_hms = r[2]
            galaxy_type = galaxy_types[np.argmax([r[-3], r[-2], r[-1]])]

            c = SkyCoord(ra_hms + ' ' + dec_hms, unit=(u.hourangle, u.deg))
            ra_deg = c.ra.degree
            dec_deg = c.dec.degree

            y, x = wcs.wcs_world2pix(ra_deg, dec_deg, 0, ra_dec_order=True)
            x, y = x + 0.0, y + 0.0
            x, y = round(x), round(y)

            # galaxyを切り出し、画像に保存
            rng = 50
            galaxy_img = img[x - 50:x + 50, y - 50:y + 50]
            plt.title('RA = {}, Dec = {}'.format(ra_deg, dec_deg))
            plt.imshow(np.log(galaxy_img.T[::-1, ::-1]), cmap='gray')
            plt.savefig('../data/galaxy-img/' + galaxy_type + '/' + str(galaxy_id), bbox_inches='tight')
            plt.close()

            obj_label = labels[x, y]
            print(obj_label, x, y)
            picked_crds = np.array(np.where(labels == obj_label)).T
            print(np.array(picked_crds).shape)
            # patch切り出し
            patch_size = 6
            height, width = img.shape
            for x, y in picked_crds:
                # patchを切り出せない場合
                if (x - patch_size < 0) or (x + patch_size >= height) \
                        or (y - patch_size < 0) or (y + patch_size >= width):
                    print('continue')    
                    continue

                patch = img[x - patch_size:x + patch_size, y - patch_size:y + patch_size]
                patches.append(patch)

            np.save('../data/galaxy-patch/' + galaxy_type + '/' + str(galaxy_id), patches)