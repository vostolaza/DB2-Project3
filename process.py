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

rootdir = './lfw'
CHUNKSIZE=5


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
                # idx.insert(i, tuple(np.concatenate((vector[0], vector[0]), axis=None)))  
                sequential[os.path.join(subdir, file)] = tuple(vector[0])
            else: sequential[os.path.join(subdir, file)] = []
            i += 1
        print(f"Personas ingresados: {i}")
        if i >= size : break
    #guardes los ordena
    #id_domento amelveov__001 {vector caratiscos}
    buildFinalIndex(f"Sequential/Sequential_{size}.json", sequential)

def buildDictionary(size):
    i = 0
    persona = {}
    for subdir, dirs, files in os.walk(rootdir):
        name = subdir[6:]
        print(i)
        for file in files:
            persona[i] = os.path.join(subdir, file)
            i += 1
        if i >= size: break
    return persona    

def knnRTree(size, k, image):
    p = index.Property()
    p.dimension = 128 #D
    p.buffering_capacity = 3#M
    p.dat_extension = 'dat'
    p.idx_extension = 'idx'
    idx = index.Index(f"RTree/RTree_{size}", properties=p)

    picture = face_recognition.load_image_file(image)
    vector = face_recognition.face_encodings(picture)
    q = tuple(vector[0])
    # print(q)
    lres = list(idx.nearest(coordinates=q, num_results=k))
    print("El vecino mas cercano de (3,3): ", lres)
    for x in lres:
        line=json.loads(linecache.getline(f"Sequential/Sequential_{size}.json", x))
        print(line[0])


def ED(vec1, vec2):
    dist = 0
    for i in range(len(vec1)):
        dist += math.pow(vec1[i] - vec2[i], 2)
    return math.sqrt(dist)

def knnSequential(size, k, image):
    iterator =iter(pd.read_json(f"Sequential/Sequential_{size}.json",lines=True,chunksize=CHUNKSIZE))
    data=next(iterator,None) 
    
    result = []
    picture = face_recognition.load_image_file(image)
    vector = face_recognition.face_encodings(picture)
    q = vector[0]
    current = -1
    while data is not None:
        current += 1
        for i in range(data.size//2): 
            x = CHUNKSIZE * current + i
            if len(data[1][x]) > 0 :
                
                d = ED(q, data[1][x])
                heapq.heappush(result, (-d, data[0][x] ))
                if ( len(result ) > k):
                    heapq.heappop(result) 
        data = next(iterator, None)
       

    result = [(i, -d) for d, i in result]
    result.sort(key=lambda tup : tup[1])
    print(result)


def RangeRTree(size, r, image):
    
    p = index.Property()
    p.dimension = 128 #D
    p.buffering_capacity = 3#M
    p.dat_extension = 'dat'
    p.idx_extension = 'idx'
    idx = index.Index(f"RTree/RTree_{size}", properties=p)

    picture = face_recognition.load_image_file(image)
    vector = face_recognition.face_encodings(picture)

    q = vector[0]
    
    bounds = []
    bounds.extend( [ i - r for i in q ])
    bounds.extend( [ i + r for i in q ])
    
    # print(bounds)
   
    setvectors = idx.intersection(bounds, objects=True)
    
    for x in setvectors:
        line=json.loads(linecache.getline(f"Sequential/Sequential_{size}.json", x))
        print(line[0])




def RangeSequential(size, r, image):

    iterator =iter(pd.read_json(f"Sequential/Sequential_{size}.json",lines=True,chunksize=CHUNKSIZE))
    data=next(iterator,None) 
    
    result = []
    picture = face_recognition.load_image_file(image)
    vector = face_recognition.face_encodings(picture)
  
    q = vector[0]
    
    bounds = []
    bounds.extend( [ i - r for i in q ])
    bounds.extend( [ i + r for i in q ])

    
    current = -1
    while data is not None:
        current += 1
        for i in range(data.size//2): 
            x = CHUNKSIZE * current + i
            if len(data[1][x]) > 0 :
                flag = 1
                for k in range(len(q)):
                    if data[1][x][k]<bounds[k] or data[1][x][k] > bounds[k+len(q)] :
                        flag = 0
                        break
                if flag == 1 : 
                    print(data[0][x])     
        data = next(iterator, None)
                



  
indexs=[100,200,400,800,1600,3200,6400,12800]



RangeSequential(100, 10, "./lfw/Aaron_Peirsol/Aaron_Peirsol_0001.jpg")
RangeRTree(100, 100, "./lfw/Aaron_Peirsol/Aaron_Peirsol_0001.jpg")
# knnRTree(6400, 8, "./lfw/Aaron_Patterson/Aaron_Patterson_0001.jpg")
# knnSequential(200, 3, "./lfw/Aaron_Patterson/Aaron_Patterson_0001.jpg")

# for indx in indexs:
#     buildFiles(rootdir, indx )
# knnSequential(100, 3, "./lfw/Adam_Scott/Adam_Scott_0001.jpg")
