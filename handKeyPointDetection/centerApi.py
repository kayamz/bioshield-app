from flask import Flask, render_template, request
import base64
import json
import time
import cv2
import os
import handPoseImage
import blurFinger
import numpy as np
import matplotlib.pyplot as plt
import requests as rq
import math
import io
from io import BytesIO
import uuid
import shutil

app = Flask(__name__) 

@app.route("/let_me_shine/results/", methods=['GET', 'POST'])
def data_return():
    global data
    if request.method == 'POST':
        data = request.get_json(silent=True)
    elif request.method == 'GET':
        data_buf = data
        data = ''
        return data_buf
    elif data == '':
        data_return.close()
    return ''

@app.route("/let_me_shine", methods=['GET', 'POST'])
def let_me_shine():
    URL_IP = 'localhost'
    URL_PORT = '12300'
    url_base = f"http://{URL_IP}:{URL_PORT}/let_me_shine/results/?uid="

    time_flag = time.strftime('%m%d-%H%M%S', time.localtime(time.time()))
    client_ip = request.remote_addr
    rand_uuid = uuid.uuid4()
    usr_ID = f'{rand_uuid}'
    # client_ip = 971020

    if request.method == 'POST':
        # print('POST START!')
        # keys = request.files.keys()
        # for each in keys:
        #     print(each)

        # f = request.files['origin']
        # # f = io.BytesIO(request.get_data())
        # # file_name = r'../testing/img/{}'.format(f.filename)
        # file_name = os.path.dirname(os.path.realpath(__file__))+'../testing/img/{}'.format(f.filename)
        # print(file_name)
        # # client_img_name = '../testing/img/{}_{}.png'.format(client_ip, time_flag)
        # client_img_name = os.path.dirname(os.path.realpath(__file__))+'../testing/img/{}_{}.png'.format(client_ip, time_flag)
        # print(client_img_name)
        # f.save(file_name)

        data = request.get_json('silent=True')
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))+'/testing/img/{rand_uuid}/'
        if os.path.isdir(BASE_DIR) is not True:
            os.makedirs(BASE_DIR, exist_ok=True)
            
        RAW_DIR = f'{BASE_DIR}raw/'
        os.mkdir(RAW_DIR)

        file_name = f'{RAW_DIR}raw_{rand_uuid}.jpg'  # 첨부한 Image가 업로드한 파일명과 형식 그대로 일단 저장될 위치를 지정한다.
        client_img_name = f'{RAW_DIR}{rand_uuid}.png' # 첨부한 Image가 png 형식으로 다시 저장될 경로와 이름을 지정한다.

        with open(file_name, 'wb') as f:  # 변수에 받아들여 놓은 Image를 파일로 저장한다.
            f.write(base64.b64decode(data['origin']))

        cnv_buffer = cv2.imread(file_name)
        cv2.imwrite(client_img_name, cnv_buffer)
        # os.remove(file_name)

        # imageData = None
        # if ('img' in request.files):
        #     print('it is in request')
        #     f = request.files['origin']
        # else:
        #     print('it is not')
        #     f = request.get_data()


    protectedImage = os.path.dirname(os.path.realpath(__file__))+'/protectedImage/newthing.jpg'
    outputImage = blurFinger(client_ip, time_flag)
    # cv2.imwrite(protectedImage,outputImage)    # 걍 한번 저장해서 확인해보려고..

    # return render_template('../App.js', resultPhoto = outputImage)

    data = {'results': {'img' : base64.b64encode(open(outputImage, 'rb').read()).decode('utf-8')}}

    json_data = json.dumps(data)

    rq.post(url_base + '{}'.format(usr_ID), json=json_data)

    # return json_data
    shutil.rmtree(BASE_DIR) # UUID 디렉터리 삭제
    return url_base + '{}'.format(usr_ID)

if __name__ == "__main__":
    print("Server Start")
    app.run('localhost', port=12300, debug=True)
