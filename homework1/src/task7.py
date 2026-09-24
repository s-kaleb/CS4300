# numpy implimentation
import numpy as np

# array mutliplication in numpy
def array_multiplication():
    numpyArray = np.array([1,2,3,4,5,6,7,8,9,10])
    print(numpyArray * numpyArray)

#matrix multiplication in numpy
def matrix_multiplication():
    npMatrix1 = np.array([[2,2], [2,2]])
    npMatrix2 = np.array([[5,2], [2,2]])
    print(npMatrix1 @ npMatrix2)

#get the shape of a matrix
def matrix_shape():
    npMatrix = np.array([[1,1,1,1],[1,1,1,1]])
    print(np.shape(npMatrix))

matrix_shape()    