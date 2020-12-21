import numpy as np
from scipy import ndimage
from pydl.photoop.photoobj import unwrap_objid
import requests
import xml.etree.ElementTree as ET
import mahotas
import re
from bs4 import BeautifulSoup
from urllib3.util import Retry
from requests.adapters import HTTPAdapter


# 画像からパワースペクトルを計算する
def get_psd2d(img):
    # 2次元FFT
    img_fft = np.fft.fft2(img)

    # 象限の入れ替え
    img_fft = np.fft.fftshift(img_fft)

    # パワースペクトル
    img_power = 20*np.log(np.abs(img_fft) + 1.0)
    
    return img_power


# パワースペクトルの半径方向の平均を計算する
def get_psd1d(psd2d):

    h = psd2d.shape[0]
    w = psd2d.shape[1]
    wc = w // 2
    hc = h // 2

    # psd2dの中心からの距離の配列を作る
    Y, X = np.ogrid[0:h, 0:w]
    r = np.hypot(X - wc, Y - hc).astype(np.int)

    # rを用いて、psd2dの半径方向の平均を計算する
    psd1d = ndimage.mean(psd2d, r, index = np.arange(0, wc + 1))

    return psd1d


# 銀河のobjidから、その銀河が含まれるfitsファイルの名前を得る
def get_fits_name_from_objid(objid, f = 'r'):

    params = unwrap_objid(objid)
    run = str(params['run'])
    camcol = str(params['camcol'])
    frame = str(params['frame'])

    fits_name = 'fpC-' + run.zfill(6) + '-' + f + camcol + '-' + frame.zfill(4) + '.fit.gz'

    return fits_name



def download_sdss_img(file_name, ra, dec, width, height, opt=''):
    dr7 = 'http://skyservice.pha.jhu.edu/DR7/ImgCutout/getjpeg.aspx'
    dr14 = 'http://skyserver.sdss.org/dr14/SkyServerWS/ImgCutout/getjpeg'
    
    response = requests.get(
        dr14,
        params={
            'ra': ra, 
            'dec': dec, 
            'width': width, 
            'height': height,
            'opt': opt
            }
    )
    
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)



def get_zernikemoments_from_img(img, radius=10):
    value = mahotas.features.zernike_moments(img, radius)
    return value



def get_z_from_objid(objid):
    sqlCmd = f'SELECT * FROM SpecObjAll WHERE bestObjId={objid}'
    # response = requests.post(
    #     'http://skyserver.sdss.org/dr7/en/tools/search/x_sql.asp',
    #     {
    #         'format': 'xml',
    #         'cmd': sqlCmd,
    #     }
    # )

    # session作成
    session = requests.Session()    
    retries = Retry(total=5,  # リトライ回数
                    backoff_factor=1,  # sleep時間
                    status_forcelist=[500, 502, 503, 504])  # タイムアウト以外でリトライするステータスコード
    session.mount('http://', HTTPAdapter(max_retries=retries))

    # postリクエスト
    response = session.post(url='http://skyserver.sdss.org/dr7/en/tools/search/x_sql.asp',
                           data={
                               'format': 'xml',
                               'cmd': sqlCmd,
                           },
                           stream=True,
                           timeout=(10.0, 30.0))
    # responseをxmlとして読み込む
    root = ET.fromstring(response.text)
    try:
        # zを探して、返す。
        return float(root[1][0].attrib['z'])
    except KeyError:  # bestObjIdとobjidが一致しない場合
        print(objid)
        return get_z_from_objid2(objid)


# bestObjId != objidの場合、使用する。HTTPリクエスト2回。
def get_z_from_objid2(objid):
    # session作成
    session = requests.Session()    
    retries = Retry(total=5,  # リトライ回数
                    backoff_factor=1,  # sleep時間
                    status_forcelist=[500, 502, 503, 504])  # タイムアウト以外でリトライするステータスコード
    session.mount('http://', HTTPAdapter(max_retries=retries))

    # specObjIdを探す
    url1 = f'http://skyserver.sdss.org/dr7/en/tools/explore/OETOC.asp?id={objid}'
    response1 = session.get(url1, stream=True, timeout=(10.0, 30.0))
    html1 = response1.text
    # soup1 = BeautifulSoup(html1, 'html.parser')
    # s1 = soup1.div.table.find_all('tr')[23].a
    # m1 = re.search('href="(.*?)"', str(s1))
    # s2 = m1[1]
    # m2 = re.search('specObjId=(.*?)&', s2)
    # specObjId = m2[1]
    m = re.search('specObjId=(.*?)&', html1)
    specObjId = m[1]

    # 取得したspecObjIdの行をSpecObjAllから取ってくる。
    sqlCmd = f'SELECT * FROM SpecObjAll WHERE specObjId={specObjId}'
    response2 = session.post(
        'http://skyserver.sdss.org/dr7/en/tools/search/x_sql.asp',
        {
            'format': 'xml',
            'cmd': sqlCmd
        },
        stream=True,
        timeout=(10.0, 30.0)
    )
    root = ET.fromstring(response2.text)
    # zを探して、返す。
    return float(root[1][0].attrib['z'])