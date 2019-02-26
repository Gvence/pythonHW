import numpy as np
import torch
from torch.autograd import Variable

tensor = torch.FloatTensor([[1,2], [3,4]])
variable = Variable(tensor, requires_grad = True)

t_out = torch.mean(tensor*tensor)
v_out = torch.mean(variable*variable)
print('tout', t_out)
print('\nv_out', v_out)
v_out.backward()
print(variable.grad)