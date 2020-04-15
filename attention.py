import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


class Attention(nn.Module):

    def __init__(self, hidden_size):
        super(Attention, self).__init__()
        
        self.hidden_size = hidden_size

    def forward(self, hidden, encoder_outputs):
        seq_len = len(encoder_outputs)
        energies = Variable(torch.zeros(seq_len))
        energies = energies.cuda()
        for i in range(seq_len):
            energies[i] = self._score(hidden, encoder_outputs[i])
        return F.softmax(energies).unsqueeze(0).unsqueeze(0)

    def _score(self, hidden, encoder_output):
      hidden=hidden.t().view(-1)
      encoder_output=encoder_output.view(-1)
      energy = hidden.dot(encoder_output)
        
      return energy