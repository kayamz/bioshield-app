from flask import Flask, render_template, request
import base64
import json
import time
import cv2
import os
from blurFinger import Finger_blur
from blurIris import iris_blur
import numpy as np
import matplotlib.pyplot as plt
import requests as rq
import uuid
import shutil

app = Flask(__name__) 

@app.route("/let_me_shine/results/", methods=['GET', 'POST'])
def data_return():
    global data
    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)
    elif request.method == 'GET':
        data_buf = data
        data = ''
        return data_buf
    elif data == '':
        data_return.close()
    return ''

@app.route("/let_me_shine", methods=['GET', 'POST'])
def let_me_shine():
    URL_IP = '172.30.1.47'
    URL_PORT = '45045'
    url_base = f'http://{URL_IP}:{URL_PORT}/let_me_shine/results/?uid='

    rand_uuid = uuid.uuid4()
    usr_ID = f'{rand_uuid}'

    try:
        data = request.get_json(silent=True, force=True)
        if not data['origin']:       
            print('Re-send image, please.')
            return 'Re-send image, please.'
        else:
            BASE_DIR = f'{os.path.dirname(os.path.realpath(__file__))}/testing/img/'

            if os.path.isdir(BASE_DIR) is not True:
                os.makedirs(BASE_DIR, exist_ok=True)

            RAW_DIR = f'{BASE_DIR}raw/'

            file_name = f'{RAW_DIR}raw_{rand_uuid}.jpg'  # 첨부한 Image가 업로드한 파일명과 형식 그대로 일단 저장될 위치를 지정한다.
            client_img_name = f'{RAW_DIR}raw.png' # 첨부한 Image가 png 형식으로 다시 저장될 경로와 이름을 지정한다.

            with open(file_name, 'wb') as f:  # 변수에 받아들여 놓은 Image를 파일로 저장한다.
                f.write(base64.b64decode(data['origin']))

            cnv_buffer = cv2.imread(file_name)
            cv2.imwrite(client_img_name, cnv_buffer)
            os.remove(file_name)

            # 여기가 진짜
            midName = ''
            midName = Finger_blur(BASE_DIR, client_img_name)
            print('mid is ', midName)

            outputName = ''
            outputName = iris_blur(BASE_DIR, midName)
            print('outputName is ', outputName)

            data = {'results' : {'after' : f'{outputName}',
                                'after64': base64.b64encode(open(outputName, 'rb').read()).decode('utf-8')}}

            json_data = json.dumps(data)

            rq.post(url_base + f'please', json=json_data)

            return url_base + f'please'

    except Exception as e:
        print(f'json_data part error: {e}')
        return f'{e}'

if __name__ == '__main__':
    print('Server Start')
    app.run('172.30.1.47', port=45045, debug=True)
