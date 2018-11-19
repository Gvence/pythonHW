import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op


def LoadData(filename):
    data = np.loadtxt(filename)
    data = np.array(data)
    return data


def ReshapeData(data):
    m = np.size(data, 0)
    X = data[:, 0:2]
    Y = data[:, 2]
    Y = Y.reshape((m, 1))
    return X, Y


def InitData(X):
    m, n = X.shape
    initial_theta = np.zeros(n + 1)
    VecOnes = np.ones((m, 1))
    X = np.column_stack((VecOnes, X))
    return X, initial_theta


def sigmoid(x):
    z = 1 / (1 + np.exp(-x))
    return z


def costFunction(theta, X, Y):
    m = X.shape[0]
    J = (-np.dot(Y.T, np.log(sigmoid(X.dot(theta)))) - \
         np.dot((1 - Y).T, np.log(1 - sigmoid(X.dot(theta))))) / m
    return J


def gradient(theta, X, Y):
    m, n = X.shape
    theta = theta.reshape((n, 1))
    grad = np.dot(X.T, sigmoid(X.dot(theta)) - Y) / m
    return grad.flatten()


if __name__ == '__main__':
    data = LoadData('ex2data1.txt')
    X, Y = ReshapeData(data)
    # fig = plt.figure(1, figsize=(10, 8), dpi=120)
    # chart = fig.add_subplot(1, 1, 1)
    # plt.title('dataMap')
    # plt.xlabel('Exam 1 score')
    # plt.ylabel('Exam 2 score')
    # plt.grid(True)
    # point1 = chart.scatter(X[np.where(Y == 0), 0], X[np.where(Y == 0), 1], c='r', marker='o')
    # point2 = chart.scatter(X[np.where(Y == 1), 0], X[np.where(Y == 1), 1], c='k', marker='+')
    # chart.legend([point1, point2], ['Not admitted', 'Admitted'], loc=0)
    X, initial_theta = InitData(X)
    result = op.minimize(fun=costFunction, x0=initial_theta, args=(X, Y), method='TNC', jac=gradient)
    # x1 =np.linspace(30,100,1000)
    # x2 = -(result.x[1]*x1 + result.x[0])/result.x[2]
    # boundaryLine = chart.plot(x1,x2,c = 'y', linestyle = '-.')
    # plt.savefig("dataMap.png")
    # plt.show()
    # print(result.jac)
    # print(result)
    exit()