from flask import Flask, request, render_template
import argparse
import base64
import json
import time
import cv2
import os
import sys
from torchvision.utils import save_image

def Finger_blur(client_ip, time_flag) :
    import handPoseImage
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    import math
    import os

    FIRST_IMAGE_DIR = os.path.dirname(os.path.realpath(__file__))+'/testing/img/'
    # MEDIUM_IMAGE_DIR = r'../image_2_style_gan/save_image/crossover/'  # Image처리 과정 도중 생성되는 중간 산물들을 임시 저장할 경로를 설정한다.
    FINAL_IMAGE_DIR = os.path.dirname(os.path.realpath(__file__))+'/protectedImage/'  # 처리 완료된 Image를 파일로 저장할 경로를 설정한다.

    if os.path.isdir(FINAL_IMAGE_DIR) is not True:
        os.makedirs(FINAL_IMAGE_DIR, exist_ok=True)
        # 경로에 해당하는 폴더가 존재하지 않는 것이 하나라도 있을 경우, 자동으로 해당 경로 전체에 해당하는 모든 폴더를 생성한다.
        # 이미 존재하는 폴더에 대해서는 오류 발생을 무시하고 과정을 진행한다.

    # if os.path.isdir(MEDIUM_IMAGE_DIR) is not True:
    #     os.makedirs(MEDIUM_IMAGE_DIR, exist_ok=True)
        # 경로에 해당하는 폴더가 존재하지 않는 것이 하나라도 있을 경우, 자동으로 해당 경로 전체에 해당하는 모든 폴더를 생성한다.
        # 이미 존재하는 폴더에 대해서는 오류 발생을 무시하고 과정을 진행한다.

    parser = argparse.ArgumentParser(description='Find latent representation of reference images using perceptual loss')

    parser.add_argument('--src_img', default=FIRST_IMAGE_DIR)

    args = parser.parse_args()


    FINAL_IMAGE_DIR = FINAL_IMAGE_DIR + client_ip + time_flag + '/'  # 결과물 Image를 저장할 경로를 Client의 IP와 작업 개시 시간을 이용해 조합한다.
    if os.path.isdir(FINAL_IMAGE_DIR) is not True:
        os.mkdir(FINAL_IMAGE_DIR)  # 해당 경로 이름으로 실제 폴더를 생성한다.

    # file_names = []
    final_name = FINAL_IMAGE_DIR + time_flag + '.png'  # 결과물 Image의 파일명을 조합한다.

    origin_name = '{}{}_origin.png'.format(FINAL_IMAGE_DIR, time_flag)
    # outputImage = os.path.dirname(os.path.realpath(__file__))+'/protectedImage/new.jpg'

    inputImage = args.src_img[0]
    img = cv2.imread(inputImage)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ksize = 10

    points = handPoseImage.detect_fingerPoint(inputImage)

    p1 = points[0]  # 4번좌표
    p2 = points[1]  # 5번좌표
    p3 = points[2]  # 8번좌표
    p4 = points[3]  # 7번좌표
    mask_img = np.zeros(img.shape, dtype='uint8')
    
    # 검지
    circle_center = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
    circle_radius = int((math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2))//3)

    print(circle_center)
    print(circle_radius)
    cv2.circle(mask_img, circle_center, circle_radius, (255, 255, 255), -1)

    img_all_blurred = cv2.blur(img, (ksize, ksize))
    img_first_blurred = np.where(mask_img > 0, img_all_blurred, img)

    # 중지
    circle_center = ((p3[0] + p4[0]) // 2, (p3[1] + p4[1]) // 2)
    circle_radius = int((math.sqrt((p3[0]-p4[0])**2 + (p3[1]-p4[1])**2))//5)

    cv2.circle(mask_img, circle_center, circle_radius, (255, 255, 255), -1)

    img_second_blurred = np.where(mask_img > 0, img_all_blurred, img_first_blurred)

    # cv2.imwrite(final_name, img_second_blurred)

    save_image(img_second_blurred, final_name)

    return final_name
    
if __name__ == '__main__':
    Finger_blur()
