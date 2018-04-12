#! /usr/bin/python3
# -*- coding: utf8 -*-


import os

import cv2

import face_recognition as fr
from numpy import ndarray

class Face_handle:
    def __init__(self, train_set: str= 'known_people_folder/'):
        self.train_set = train_set
        self.names = []
        self.known_face = []
        self.load_data()

    def load_data(self):
        labels = os.listdir(self.train_set)
        for label in labels:
            if label not in self.names:
                self.names.append(label)
                fullpath = self.train_set + label
                image = fr.load_image_file(fullpath)
                face_encoding = fr.face_encodings(image)
                if len(face_encoding) > 1:
                    return False, label
                self.known_face.append(face_encoding[0])
        return True

    def recognise(self, frame: ndarray) -> (str, (int, int, int, int)):
        bounding_box = fr.face_locations(frame)
        encoding = fr.face_encodings(frame)
        if len(encoding) == 0 or len(bounding_box) == 0:
            pass
        recognise_result = fr.compare_faces(self.known_face, encoding[0])
        try:
            name_index = recognise_result.index(True)
        except ValueError:
            return None, None
        return self.names[name_index].split('.')[0], bounding_box[0]

    def has_people(self, name: str):
        return name in self.names
