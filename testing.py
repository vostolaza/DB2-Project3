import search
import time


def timeRTreeKNN(size):
    tic = time.perf_counter()
    search.knnRTree(size, 8, "./static/lfw/Phil_Mickelson/Phil_Mickelson_0001.jpg")
    toc = time.perf_counter()
    print(f"RTree KNN with {size} elements finished in  {toc - tic:0.4f} seconds")

def timeSequentialKNN(size):
    tic = time.perf_counter()
    search.knnSequential(size, 8, "./static/lfw/Phil_Mickelson/Phil_Mickelson_0001.jpg")
    toc = time.perf_counter()
    print(f"Sequential KNN with {size} elements finished in  {toc - tic:0.4f} seconds")

def timeRangeRTree(size):
    tic = time.perf_counter()
    search.RangeRTree(size, 5, "./static/lfw/Phil_Mickelson/Phil_Mickelson_0001.jpg")
    toc = time.perf_counter()
    print(f"RTree Range search with {size} elements and radius 5 finished in  {toc - tic:0.4f} seconds")

def timeRangeSequential(size):
    tic = time.perf_counter()
    search.RangeSequential(size, 5, "./static/lfw/Phil_Mickelson/Phil_Mickelson_0001.jpg")
    toc = time.perf_counter()
    print(f"Sequential Range search with {size} elements and radius 5 finished in  {toc - tic:0.4f} seconds")

sizes = [100, 200, 400, 800, 1600]

for size in sizes:
    timeRTreeKNN(size)
    timeSequentialKNN(size)
    timeRangeRTree(size)
    timeRangeSequential(size)