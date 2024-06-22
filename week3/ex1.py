
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class Softmax(nn.Module):
    """Softmax"""
    def __init__(self, stable=False):
        super(Softmax, self).__init__()
        self.stable=stable

    def forward(self, x:torch.Tensor, dim=-1):
        if not self.stable:
            x = torch.exp(x)
            sum = x.sum(dim=dim) 
        else:
            c = torch.max(x, dim=dim) 
            x = torch.exp(x - c)
            sum = x.sum(dim=dim) 
        
        return x/sum

        