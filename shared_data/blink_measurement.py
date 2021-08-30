"""
Blink measurement

Reference:
    1.EAR(eyes aspect ratio)：http://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf
    2.high speed blink detection (opencv + dlib)：https://qiita.com/mogamin/items/a65e2eaa4b27aa0a1c23    
"""
import os
import cv2
import dlib
import time
import numpy as np
from imutils import face_utils
from scipy.spatial import distance
from scipy import signal


# web camera
DEVICE_ID = 0
WIDTH = 640
HEIGHT = 480
FPS = 20


display_size = 300

def blink_detect():
    cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("H","2","6","4")) # webcam logicool C920
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M","J","P","G")) # webcam logicool C270
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    face_parts_detector = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    blink_list = [0] * (FPS * 60) # frame/min

    def calc_ear(eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        eye_ear = (A + B) / (2.0 * C)
        return round(eye_ear, 3)

    def eye_marker(face_mat, position):
        for i, ((x, y)) in enumerate(position):
            cv2.circle(face_mat, (x, y), 1, (255, 255, 255), -1)
            cv2.putText(face_mat, str(i), (x + 2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

    def calc_blink(blink_list):
        blink_array = np.array(blink_list)
        num = 3 # blink_speed(0.10~0.15s) / FPS(20Hz) = 2~3  → 3(for slow blink)
        b = np.ones(num)/num
        blink_array_ma = np.convolve(blink_array, b, mode="same")

        # Count Close(0→+x)
        close_cnt = 0
        for i in range(blink_array_ma.size-1):
            val1 = blink_array_ma[i]
            val2 = blink_array_ma[i+1]
            if val1 == 0 and val2 > 0:
                close_cnt += 1
        return close_cnt
        

    while True:
        start = time.time()
        tick = cv2.getTickCount()
        
        ret, rgb = cap.read()

        #scale = display_size / rgb.shape[0]
        #rgb = cv2.resize(rgb, dsize=None, fx=scale, fy=scale)

        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.11, minNeighbors=3, minSize=(100, 100))

        if len(faces) == 1:
            x, y, w, h = faces[0, :]
            cv2.rectangle(rgb, (x, y), (x + w, y + h), (255, 0, 0), 2)

            face_gray = gray[y :(y + h), x :(x + w)]
            scale = display_size / h
            face_gray_resized = cv2.resize(face_gray, dsize=None, fx=scale, fy=scale)
            
            
            face = dlib.rectangle(0, 0, face_gray_resized.shape[1], face_gray_resized.shape[0])
            face_parts = face_parts_detector(face_gray_resized, face)
            face_parts = face_utils.shape_to_np(face_parts)

            left_eye = face_parts[42:48]
            eye_marker(face_gray_resized, left_eye)

            left_eye_ear = calc_ear(left_eye)
            cv2.putText(rgb, "LEFT eye EAR:{} ".format(left_eye_ear), 
                (5, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1, cv2.LINE_AA)

            right_eye = face_parts[36:42]
            eye_marker(face_gray_resized, right_eye)

            right_eye_ear = calc_ear(right_eye)
            cv2.putText(rgb, "RIGHT eye EAR:{} ".format(round(right_eye_ear, 3)), 
                (5, 75), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1, cv2.LINE_AA)

            if (left_eye_ear + right_eye_ear) < 0.55:
                cv2.putText(rgb,"Blink!",
                    (5,90), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1, 1)
                blink_list.pop(0)
                blink_list.append(1)
            else:
                blink_list.pop(0)
                blink_list.append(0)

            cv2.imshow('frame_resize', face_gray_resized)

            
        else:
            blink_list.pop(0)
            blink_list.append(0)

        blink_rate = calc_blink(blink_list)

        cv2.putText(rgb,"blink_rate[1/min]:{}".format(blink_rate),
                    (5,105), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1, 1)
        if blink_rate <= 10:
            cv2.putText(rgb,"Less blinking !",
                    (5,130), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2, 1)
        elif blink_rate >= 40:
            cv2.putText(rgb,"Possible dry eye !",
                    (5,130), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2, 1)
        else:
            pass

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - tick)
        cv2.putText(rgb, "FPS:{} ".format(int(fps)), 
            (5, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('frame', rgb)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
        
        end = time.time() - start
        while end <= (1/FPS):
            end = time.time() - start

    cap.release()
    cv2.destroyAllWindows()





if __name__ == '__main__':
    blink_detect()