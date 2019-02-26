import numpy as np
import scipy.optimize as op
import matplotlib.pyplot as plt
import os

def loadData (filename):
    data = np.loadtxt(filename)
    data = np.array(data)
    return data

def indexBia (X):
    m = np.size(X, 1)
    X = np.row_stack(((np.ones((1,m))), X))
    return X

def reshapeData(data):
    m = np.size(data, 0)
    n = np.size(data, 1)
    print('MxN = ', m, 'X', n)
    X = np.array(data[:, 0 : n - 1])#列取值0 1 2 3， n-1 =4，左闭右开取值
    Y = np.array(data[:, n - 1]).reshape((m,1))
    Y = np.where(Y == 1, [1, 0, 0], Y)
    Y = np.where(Y == 2, [0, 1, 0], Y)
    Y = np.where(Y == 3, [0, 0, 1], Y)
    # print(Y)
    return X, Y

def sigmoid(Z):
    unitValue = 1/(1 + np.exp( -Z))
    return unitValue

def initparaments (L_0, L_1, L_2, feature_num, option):
    if option == 'theta':
        parament = np.random.rand((feature_num + 1) * L_0 + (L_0 + 1) * L_1 + (L_1 + 1) * L_2)\
                *(2*INIT_EPSILON) - INIT_EPSILON
    elif option == 'delta':
        parament = np.random.rand((feature_num + 1) * L_0 + (L_0 + 1) * L_1 + (L_1 + 1) * L_2)
    else:
        parament = np.zeros((feature_num + 1) * L_0 + (L_0 + 1) * L_1 + (L_1 + 1) * L_2)

    parament_0 = parament[0 : L_0 * (feature_num + 1)].reshape((L_0, (feature_num + 1)))

    parament_1 = parament[L_0 * (feature_num + 1) : \
                    (L_0 * (feature_num + 1) + (L_0 + 1) * L_1)].reshape((L_1, L_0 + 1))

    parament_2 = parament[(L_0 * (feature_num + 1) + (L_0 + 1) * L_1) : \
                    ((feature_num + 1) * L_0 + (L_0 + 1) * L_1 + (L_1 + 1) * L_2)].reshape((L_2, L_1 + 1)) #拆分

    return np.array([parament_0, parament_1, parament_2])

def forwardProp (ctheta, clayerUint):
        clayerUint = indexBia(clayerUint)
        Z = np.dot(ctheta, clayerUint)
        tlayerUint = sigmoid(Z)
        return tlayerUint, Z

def computUnitValue (theta, X) :
    a0, z0 = forwardProp(theta[0], X)
    a1, z1 = forwardProp(theta[1], a0)
    a2, z2 = forwardProp(theta[2], a1)
    return np.array([a0, a1, a2]), np.array([z0, z1, z2])

def backwardProp (ttheta, clayerDelta, tunitValue):
    m, n = np.shape(tunitValue)
    tunitValue = indexBia(tunitValue)
    tlayerDelta =  np.multiply(np.dot(ttheta.T, clayerDelta), np.multiply\
                                                            (tunitValue, (np.ones(( (m + 1), n)) - tunitValue)))
    return tlayerDelta

def computDelta (theta, unitValue, Y):
    delta2 = unitValue[2] - Y
    delta1 = backwardProp(theta[2], delta2, unitValue[1])
    delta0 = backwardProp(theta[1], delta1[1:, :], unitValue[0])
    return np.array([delta0, delta1, delta2])

def computeGradient (Delta, unitValue, theta, tempDelta, LAMBDA, X):
    X = indexBia(X)
    unitValue[0] = indexBia(unitValue[0])
    unitValue[1] = indexBia(unitValue[1])
    n, m = np.shape(X)
    Delta0 = Delta[0] + np.dot(tempDelta[0][1:, :], X.T)
    Delta1 = Delta[1] + np.dot(tempDelta[1][1:, :], unitValue[0].T)
    Delta2 = Delta[2] + np.dot(tempDelta[2], unitValue[1].T)
    D0 = Delta0/m + LAMBDA*theta[0]
    D1 = Delta1/m + LAMBDA*theta[1]
    D2 = Delta2/m + LAMBDA*theta[2]
    D0[:, 0] = Delta0[:, 0]/m
    D1[:, 0] = Delta1[:, 0]/m
    D2[:, 0] = Delta2[:, 0]/m
    return np.array([Delta0, Delta1, Delta2]), np.array([D0, D1, D2])
def costFunction(unitValue, Y, theta):
    n, m = np.shape(unitValue)
    A = (np.concatenate((theta[0].reshape(20),theta[1].reshape(30),\
                        theta[2].reshape(21)))).flatten() #重构
    cost = -(np.sum(np.multiply(Y.T, np.log(unitValue)) + \
         np.multiply((1 - Y).T, np.log(1 - unitValue)))) / m
    return cost

def saveArray(filename, data):
    file = open(filename, 'wb')
    np.save(file, theta)
    file.close()
    file = open(filename, 'rb')
    save_data = np.load(file)
    file.close()
    print(save_data,'\n',
          filename,'\n',
          'SAVED IN CURRENT DIRECTORY!!','\n')

def weightsCheckOut(weight, X):
    unitValue, z = computUnitValue(weight, X.T)
    return unitValue[2]




if __name__ == '__main__':
#网络参数初始化
    Layer_num = 3
    Unit_L0 = 4
    Unit_L1 = 6
    Unit_L2 = 3
    INIT_EPSILON = 1
    LAMBDA = 2.56
    ALPHA = 0.001
    ITERATION = 15000

#网络数据初始化
    load_data = loadData('setdata.txt')
    cost = []
    X, Y = reshapeData(load_data)
    feature_num = np.size(X.T, 0)
    theta = initparaments(Unit_L0, Unit_L1, Unit_L2, feature_num, 'theta')
    Delta = initparaments(Unit_L0, Unit_L1, Unit_L2, feature_num, 'delta')

#开始训练
    for i in range(ITERATION):
        unitValue, z = computUnitValue(theta, X.T)
        tempDelta = computDelta(theta, unitValue, Y.T)
        Delta, D = computeGradient(Delta, unitValue, theta, tempDelta, LAMBDA, X.T)
        theta = theta - ALPHA*D
        cost = np.append(cost, costFunction(unitValue[2], Y, theta))

#保存训练好的权重
    saveArray('Theta.npy', theta)
    np.savetxt('theta0.txt', theta[0])
    np.savetxt('theta1.txt', theta[1])
    np.savetxt('theta2.txt', theta[2])

#载入需要测试的权重
    weights = np.load('Theta.npy')#
    test_data = loadData('test.txt')
    X, Y = reshapeData(test_data)
    result = weightsCheckOut(weights, X)
    print(np.around(np.column_stack((result.T,Y)), decimals=2))

#绘制误差图
    fig = plt.figure(1, figsize=(10, 8), dpi=120)
    chart = fig.add_subplot(1, 1, 1)
    x1 = np.arange(0,ITERATION, 1)
    x2 = cost
    costLine = chart.plot(x1,x2,c = 'y', linestyle = '-.')
    plt.xlabel('iteration')
    plt.ylabel('cost')
    plt.title('costLine')
    plt.savefig("costLine.png")
    plt.show()