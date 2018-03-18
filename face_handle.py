#! /usr/bin/python3
# -*- coding: utf8 -*-


import os

import face_recognition as fr
from numpy import ndarray

class Face_handle:
    def __init__(self):
        self.names = []
        self.known_face = []
        self.load_data()

    def load_data(self):
        prefix = "known_people_folder/"
        labels = os.listdir(prefix)
        for label in labels:
            if label not in self.names:
                self.names.append(label)
                fullpath = prefix + label
                image = fr.load_image_file(fullpath)
                face_encoding = fr.face_encodings(image)
                if len(face_encoding) > 1:
                    return False, label
                self.known_face.append(face_encoding[0])
        return True

    def recognise(self, frame: ndarray):
        bounding_box = fr.face_locations(frame)
        encoding = fr.face_encodings(frame)
        recognise_result = fr.compare_faces(self.known_face, encoding[0])
        try:
            name_index = recognise_result.index(True)
        except ValueError:
            return None
        return self.names[name_index].split('.')[0], bounding_box[0]

    def has_people(self, name: str):
        return name in self.names
