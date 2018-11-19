import numpy as np
import scipy.optimize as op
import matplotlib.pyplot as plt


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
    Y = np.array(data[:, n - 1]).reshape((150,1))
    Y = np.where(Y == 1, [1, 0, 0], Y)
    Y = np.where(Y == 2, [0, 1, 0], Y)
    Y = np.where(Y == 3, [0, 0, 1], Y)
    # print(Y)
    return X, Y

def sigmoid(Z):
    unitValue = 1/(1 + np.exp( - Z))
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

def backwardProp (ttheta, clayerDelta, z):
    m, n = np.shape(z)
    z = np.row_stack(((np.ones((1, n))), z))
    tlayerDelta = np.multiply(np.dot(ttheta, clayerDelta), np.multiply(z, (np.ones((( m + 1), n)) - z)))
    return tlayerDelta

def computDelta (theta, output, Y, z):
    delta2 = output - Y
    delta1 = backwardProp(theta[2].T, delta2, z[1])
    delta0 = backwardProp(theta[1].T, delta1[1:, :], z[0])
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
if __name__ == '__main__':
    Layer_num = 3
    Unit_L0 = 4
    Unit_L1 = 6
    Unit_L2 = 3
    INIT_EPSILON = 1
    LAMBDA = 1000
    ALPHA = 0.001
    ITERATION = 100
    data = loadData('setdata.txt')
    cost = []
    X, Y = reshapeData(data)
    feature_num = np.size(X.T, 0)
    theta = initparaments(Unit_L0, Unit_L1, Unit_L2, feature_num, 'theta')
    Delta = initparaments(Unit_L0, Unit_L1, Unit_L2, feature_num, 'delta')
    for i in range(ITERATION):
        unitValue, z = computUnitValue(theta, X.T)
        tempDelta = computDelta(theta, unitValue[2], Y.T, z)
        Delta, D = computeGradient(Delta, unitValue, theta, tempDelta, LAMBDA, X.T)
        theta = theta - ALPHA*D
        cost = np.append(cost, costFunction(unitValue[2], Y, theta))
        testFlag = theta[2]
        print(testFlag,'\n\n\n\n\n')

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