
import torch
import torch.nn as nn


class Softmax(nn.Module):
    """Softmax"""

    def __init__(self, stable=False):
        super(Softmax, self).__init__()
        self.stable = stable

    def forward(self, x: torch.Tensor, dim=-1):
        if not self.stable:
            x = torch.exp(x)
            out = x.sum(dim=dim)
        else:
            c = torch.max(x, dim=dim)
            x = torch.exp(x - c)
            out = x.sum(dim=dim)

        return x/out
