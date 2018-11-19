import matplotlib.pyplot as plt
import numpy as NP
import scipy.optimize as op

def sigmoid(x):
    z=1/(1+NP.exp(-x))
    return z

def gradient (theta, X, Y):
    grad = NP.dot((sigmoid(-NP.dot(X, theta)) - Y).T, X)/ m
    return grad

def costFunction (theta, X, Y):
    cost = (-NP.dot((NP.log(sigmoid(-NP.dot(X,theta)))).T, Y) - NP.dot((NP.log(1 - sigmoid(-NP.dot(X,theta)))).T, (1 -Y)))/m
    grad = gradient(theta, X, Y)
    return cost, grad


if __name__ == '__main__':
    iteration = 1500
    alpha = 0.1
    data = NP.loadtxt('ex2data1.txt', dtype=NP.float32)
    data = NP.array(data)
    X = data[:, (0,1)]
    Y = data[:, 2].reshape(100, 1)

    m, n = X.shape
    X = NP.column_stack((NP.ones([m,1]),X))
    theta = NP.zeros(n+1)
    cost, grad = costFunction(theta, X, Y)
    print('cost:'+'\n',cost,'\n'+'grad:'+'\n', grad)
    result = op.minimize(fun = costFunction, x0=theta, args=(X, Y), method='TNC', jac=gradient)
    print(result)

