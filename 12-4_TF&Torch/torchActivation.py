import torch
import torch.nn.functional as Func
from torch.autograd import Variable
import matplotlib.pyplot as plt

x = torch.unsqueeze(torch.linspace(-1, 1, 100), dim = 1)
y = x.pow(2) + 0.2 * torch.rand(x.size())

x, y = Variable(x), Variable(y)

# plt.scatter(x.data.numpy(), y.data.numpy())
# plt.show()

class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden, n_output)
        self.predict = torch.nn.Linear(n_hidden, 1)

    def forward(self, x):
        x = Func.relu(self.hidden(x))
        x = self.predict(x)
        return x

if __name__ == '__main__':
    net = Net(1, 10, 1)
    print(net)
    plt.ion()
    plt.show()
    optimizer = torch.optim.SGD(net.parameters(), lr = 0.1)
    loss_func = torch.nn.MSELoss()#均方差
    for i in range (100):
        prediction = net(x)

        loss = loss_func(prediction, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if i % 5 == 0:
            plt.cla()
            plt.scatter(x.data.numpy(), y.data.numpy())
            plt.plot(x.data.numpy(), prediction.data.numpy(), 'r-', lw = 5)
            plt.text(0.5, 0, 'Loss = %.4f' % loss.data[0], fontdict = {'size': 20, 'color': 'red'})
            plt.pause(0.1)
    plt.savefig("torch_regression")
    plt.ioff()