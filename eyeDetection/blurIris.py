def iris_blur(BASE_DIR, client_img_name) :
    import blurFinger
    from torchvision.utils import save_image
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    import math
    import os

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    FINAL_IMAGE_DIR = f'{BASE_DIR}final/'
    if os.path.isdir(FINAL_IMAGE_DIR) is not True:
        os.makedirs(FINAL_IMAGE_DIR, exist_ok=True)

    final_name = f'{FINAL_IMAGE_DIR}after.png'

    img = cv2.imread(client_img_name)

    # fingerDoneImageName = blurFinger.Finger_blur(BASE_DIR, client_img_name)
    # print(fingerDoneImageName)
    # img = cv2.imread(fingerDoneImageName)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ksize = 10
    tmp = 0

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_color = img[y:y + h, x:x + w]
        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            p1 = (x+ex+5, y+ey)
            p2 = (p1[0] + ew, p1[1] + eh)

            circle_center = ((p1[0] + p2[0])// 2, (p1[1] + p2[1]) // 2)
            circle_radius = int(math.sqrt(ew*2 + eh*2) // 2)
            mask_img = np.zeros(img.shape, dtype='uint8')
            cv2.circle(mask_img, circle_center, circle_radius, (255, 255, 255), -1)

            img_all_blurred = cv2.blur(img, (ksize, ksize))

            if tmp == 0:
                img_first_blurred = np.where(mask_img > 0, img_all_blurred, img)
                tmp += 1
            
            else :
                img_second_blurred = np.where(mask_img > 0, img_all_blurred, img_first_blurred)
                tmp += 1

    if tmp == 1:
        cv2.imwrite(final_name,img_first_blurred)

    elif tmp == 2:
        cv2.imwrite(final_name,img_second_blurred)
        print('Iris Detection Done')

    else :
        cv2.imwrite(final_name,img)
        print('There is  no iris.')

    return final_name
    
if __name__ == '__main__':
    iris_blur()