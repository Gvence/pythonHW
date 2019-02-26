import numpy as np
import matplotlib.pyplot as plt

#Data
x = np.arange(1, 100)
y = x * 2

def model(a, b, x):
    return a*x + b

def cost_function(a, b, x, y):
    n = 5
    return 0.5/n * (np.square(y-a*x-b)).sum()

def optimize(a,b,x,y):
    n = 5
    alpha = 1e-1
    y_hat = model(a,b,x)
    da = (1.0/n) * ((y_hat-y)*x).sum()
    db = (1.0/n) * ((y_hat-y).sum())
    a = a - alpha*da
    b = b - alpha*db
    return a, b
plt.ion()
plt.show()
if __name__ == '__main__':
    a=1
    b=1
    for i in range (50):
        a, b = optimize(a, b, x, y)
        plt.cla()
        plt.scatter(x, y)
        plt.plot(x, x*a + b, 'b--')
        plt.pause(0.3)
    plt.ioff()
    plt.show()