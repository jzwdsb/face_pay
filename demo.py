#! /usr/bin/python3
#  -*- coding:utf8 -*-

__author__ = 'manout'

import cv2
import face_recognition


cap = cv2.VideoCapture(0)
cv2.namedWindow("video", 0)

'分辨率太高会导致视频卡顿，可以降低分辨率至 320 * 240, 可以得到流畅'
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
while True:
    ret, frame = cap.read()
    face_locations = face_recognition.face_locations(frame)
    for face in face_locations:
        top, right, bottom, left = face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 3)
    cv2.imshow("video", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
