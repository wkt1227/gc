# -*- coding: utf-8 -*-
from astropy.table import Table
import astropy.wcs
import astropy.io.fits
from astropy.coordinates import SkyCoord
from astropy import units as u
from pydl.photoop.photoobj import unwrap_objid
import numpy as np
import matplotlib.pyplot as plt

DEG_CORRESPONDING_TO_5S = 0.00138889

def main():
    gz_table = Table.read('../data/GalaxyZoo1_DR_table2.fits')
    mx_x, mn_x, mx_y, mn_y = 0, 1001001001, 0, 1001001001

    # Galaxy Zooの表の上から n行目までを順に取り出す
    for galaxy_info in gz_table:

        # Galaxy Zooの表からobjid, ra, decを取り出す
        objid = galaxy_info[0]
        ra_hms = galaxy_info[1]
        dec_hms = galaxy_info[2]

        # ra,decを60進数から10進数に変換
        c = SkyCoord(ra_hms + ' ' + dec_hms, unit=(u.hourangle, u.deg))
        ra_deg = c.ra.degree
        dec_deg = c.dec.degree

        # objidからfitsファイルを特定する情報を取り出す
        params = unwrap_objid(objid)
        run = str(params['run'])
        camcol = str(params['camcol'])
        frame = str(params['frame'])

        # objidの銀河が含まれるfitsファイルを開く
        fits = astropy.io.fits.open('/media/wkt1227/ec0839a8-1d89-4192-a30f-77387e2e2c04/data_rbands/' + run.zfill(6) + '/fpC-' + run.zfill(6) + '-r' + camcol + '-' + frame.zfill(4) + '.fit.gz')
        data = fits[0].data
        header = fits[0].header
        
        # fitsファイルのheaderと銀河のra, decから,
        # 画像内の座標を得る
        wcs = astropy.wcs.WCS(header)
        px, py = wcs.wcs_world2pix(ra_deg, dec_deg, 0, ra_dec_order=True)
        px = int(px)
        py = int(py)
        
        mx_x = max(mx_x, px)
        mn_x = min(mn_x, px)
        mx_y = max(mx_y, py)
        mn_y = min(mn_y, py)

    print(data.shape)
    print(mx_x, mn_x)
    print(mx_y, mn_y)
        
if __name__ == '__main__':
    main()