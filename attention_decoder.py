import torch
import torch.nn as nn
import torch.nn.functional as F
from attention import Attention
import os
from torch.autograd import Variable

class AttentionDecoder(nn.Module):
    def __init__(self, hidden_size, output_size, n_layers=3, dropout_p=0.1):
        super(AttentionDecoder, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers
        self.dropout_p = dropout_p

        self.embedding = nn.Embedding(output_size, hidden_size)
        self.gru = nn.GRU(hidden_size * 2, hidden_size, n_layers, dropout=dropout_p)
        self.linear = nn.Linear(hidden_size * 2, output_size)
        self.attention = Attention( hidden_size)

    def forward(self, word_input, last_context, last_hidden, encoder_outputs):
        word_embedded = self.embedding(word_input).view(1, 1, -1)
        rnn_input = torch.cat((word_embedded, last_context.unsqueeze(0)), 2)
        rnn_output, hidden = self.gru(rnn_input, last_hidden)

        attention_weights = self.attention(rnn_output.squeeze(0), encoder_outputs)
        context = attention_weights.bmm(encoder_outputs.transpose(0, 1))

        rnn_output = rnn_output.squeeze(0)
        context = context.squeeze(1)
        output = F.log_softmax(self.linear(torch.cat((rnn_output, context), 1)))
        return output, context, hidden, attention_weights

    def initHidden(self):
        result = Variable(torch.zeros(1, 1, self.hidden_size))
        result = result.cuda()
        return result