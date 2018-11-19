import numpy as np
import scipy.optimize as op
import matplotlib.pyplot as plt


def loadData (filename):
    data = np.loadtxt(filename)
    data = np.array(data)
    return data

def indexBia (X):
    m = np.size(X, 0)
    X = np.column_stack(((np.ones((m, 1))), X))
    return X

def reshapeData(data):
    m = np.size(data, 0)
    n = np.size(data, 1)
    print('MxN = ', m, 'X', n)
    X = np.array(data[:, 0 : n - 1])#列取值0 1 2 3， n-1 =4，左闭右开取值
    Y = np.array(data[:, n - 1]).reshape((150,1))
    Y = np.where(Y == 1, [1, 0, 0], Y)
    Y = np.where(Y == 2, [0, 1, 0], Y)
    Y = np.where(Y == 3, [0, 0, 1], Y)
    print(Y)
    return X, Y

def sigmoid(Z):
    hx = 1/(1 + np.exp( - Z))
    return Z

def initTheta (L_0, L_1, L_2, feature_num):
    theta = np.random.rand((feature_num + 1) * L_0 + (L_0 + 1) * L_1 + (L_1 + 1) * L_2)\
            *(2*INIT_EPSILON) - INIT_EPSILON

    theta_0 = theta[0 : L_0 * (feature_num + 1)].reshape((L_0, (feature_num + 1)))

    theta_1 = theta[L_0 * (feature_num + 1) : \
                    (L_0 * (feature_num + 1) + (L_0 + 1) * L_1)].reshape((L_1, L_0 + 1))

    theta_2 = theta[(L_0 * (feature_num + 1) + (L_0 + 1) * L_1) : \
                    ((feature_num + 1) * L_0 + (L_0 + 1) * L_1 + (L_1 + 1) * L_2)].reshape((L_2, L_1 + 1)) #拆分
    return theta, theta_0, theta_1, theta_2

def forwardProp (theta, layerUint):
        layerUint = indexBia(layerUint)
        tlayerUint = np.dot(theta, layerUint.T)
        return tlayerUint

if __name__ == '__main__':
    Layer_num = 3
    Unit_L0 = 4
    Unit_L1 = 6
    Unit_L2 = 3
    INIT_EPSILON = 1
    data = loadData('setdata.txt')
    X , Y = reshapeData(data)
    feature_num = np.size(X, 1)
    inital_theta ,theta_0, theta_1, theta_2 = \
        initTheta(Unit_L0, Unit_L1, Unit_L2, feature_num)
    testFlag = forwardProp(theta_0, X)
    print(testFlag)
    # A = (np.concatenate((theta_0.reshape(20),theta_1.reshape(30),\
    #                     theta_2.reshape(21)))).flatten() #重构
    # print(A)
    print('X',np.shape(X),'Y',np.shape(Y))