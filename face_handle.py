#! /usr/bin/python3
# -*- coding: utf8 -*-


import os

import cv2
import pymysql

import face_recognition as fr
from numpy import ndarray


class Face_handle:
    def __init__(self, train_set: str, connect: pymysql.connections):
        if train_set is None:
            self.train_set = 'known_people_folder/'
        else:
            self.train_set = train_set
        self.connect = connect
        self.names = []
        self.known_face = []
        self.connect_database()
        self.load_data()

    def connect_database(self):
        with self.connect.cursor() as cursor:
            sql = 'SELECT `user_name` FROM `client_record`'
            cursor.execute(sql)
            row = cursor.fetchone()
            while row is not None:
                self.names.append(row[0])
                row = cursor.fetchone()

    def load_data(self) -> bool:
        labels = os.listdir(self.train_set)
        new_labels = []
        for name in self.names:
            find_ret = [x for x in labels if x.startswith(name)]
            if len(find_ret) == 1:
                new_labels.extend(find_ret)
        labels = new_labels
        for label in labels:
            fullpath = self.train_set + label
            image = fr.load_image_file(fullpath)
            face_encoding = fr.face_encodings(image)
            if len(face_encoding) > 1:
                return False
            self.known_face.append(face_encoding[0])
        return True

    def recognise(self, frame: ndarray) -> (str, (int, int, int, int)):
        bounding_box = fr.face_locations(frame)
        encoding = fr.face_encodings(frame)
        if len(encoding) == 0 or len(bounding_box) == 0:
            return None, '未识别到人脸'
        recognise_result = fr.compare_faces(self.known_face, encoding[0], tolerance=0.4)
        try:
            name_index = recognise_result.index(True)
        except ValueError:
            return None, '此人不在数据库中'
        return self.names[name_index], bounding_box[0]

    def add_new_client(self, frame: ndarray, name: str):
        cv2.imwrite(self.train_set + name + '.bmp', frame)
        bound_box = fr.face_locations(frame)
        encoding = fr.face_encodings(frame)
        self.names.append(name)
        self.known_face.append(encoding[0])
        return bound_box[0]

    def has_people(self, name: str):
        return name in self.names
