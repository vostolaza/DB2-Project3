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

CHUNKSIZE=5

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

    if not len(q): return []

    lres = list(idx.nearest(coordinates=q, num_results=k))
    res = []
    for x in lres:
        line=json.loads(linecache.getline(f"Sequential/Sequential_{size}.json", x+1))
        res.append(line[0])
    return res

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

    if not len(q): return []

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
    return result

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

    res = []
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
                    res.append(data[0][x])     
        data = next(iterator, None)
    return res

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
       
    lres = [n.id for n in idx.intersection(bounds, objects=True)] 

    res = []
    for x in lres:
        line=json.loads(linecache.getline(f"Sequential/Sequential_{size}.json", x+1))
        res.append(line[0])
    return res