import heapq
import json
import linecache
import math
import os
import sys
import collections
from itertools import chain

import face_recognition
import numpy as np
import pandas as pd
from rtree import index

rootdir = './static/lfw'

def buildFinalIndex(index_file,d):
    # word, data
    text=""
    for i,data in enumerate(d.items()):
        w = [data[0],data[1]]
        text+=json.dumps(w,ensure_ascii=False)
        text+="\n" if i!=len(d.items())-1 else ""
    outputData(index_file,text)

def outputData(outputfile, data):
    if not os.path.isfile(outputfile):
        out = open(outputfile, 'w')
        # out.reconfigure(encoding='utf-8')
    else:
        out = open(outputfile, 'a')
        # out.reconfigure(encoding='utf-8')
    print(data, file=out)


def buildFiles(rootdir, size):
    p = index.Property()
    p.dimension = 128 #D
    p.buffering_capacity = 3#M
    p.dat_extension = 'dat'
    p.idx_extension = 'idx'
    idx = index.Index(f'RTree/RTree_{size}',properties=p)

    sequential = {}

    i = 0
    for subdir, dirs, files in os.walk(rootdir):
        print(subdir)
        for file in files:
            picture = face_recognition.load_image_file(os.path.join(subdir, file))
            vector = face_recognition.face_encodings(picture)
            if len(vector) > 0:
                idx.insert(i, tuple(np.concatenate((vector[0], vector[0]), axis=None)))  
                sequential[os.path.join(subdir, file)] = tuple(vector[0])
            else: sequential[os.path.join(subdir, file)] = []
            i += 1
        print(f"Personas ingresados: {i}")
        if i >= size : break
    buildFinalIndex(f"Sequential/Sequential_{size}.json", sequential)

indexs=[100, 6400,12800]

for indx in indexs:
    buildFiles(rootdir, indx )