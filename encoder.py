import torch
import torch.nn as nn
from torch.autograd import Variable
from language import Language
import pickle
import numpy as np

class EncoderRNN(nn.Module):

    def __init__(self, input_size, hidden_size, input_lang,n_layers=3,lang="insta"):
        super(EncoderRNN, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.n_layers = n_layers

        self.embedding = nn.Embedding(input_size, hidden_size)
        # with open('data/vocab1.bin', 'rb') as f:
        #   pretrain_vocab = pickle.load(f)
        pretrain_vocab=[]
        # with open('data/vectors1.bin', 'rb') as f:
        #   pretrain_vectors = pickle.load(f) 
        pretrained_weight = []
        cnt = 0
        for i in range(input_size):
            word=input_lang.index2word[i]
            if word in pretrain_vocab:
                vector = pretrain_vectors[pretrain_vocab.index(word)] 
            else:
              temp = np.zeros(300)
              for subword in word:
                if subword in pretrain_vocab:
                    vector = pretrain_vectors[pretrain_vocab.index(subword)] 
                    temp += vector
                else :
                  vector = np.random.normal(loc=0.0, scale=1.0, size=[300,])
                  temp += vector
              temp = temp/len(word)
              vector = temp
            # else:
            #     vector = np.random.normal(loc=0.0, scale=1.0, size=[300,])
            #     cnt += 1
            pretrained_weight.append(vector)
        pretrained_weight = np.array(pretrained_weight,dtype = np.float32)
        self.embedding.weight.data.copy_(torch.from_numpy(pretrained_weight))
        print('the number of unkown words :',cnt)
        self.gru = nn.GRU(hidden_size, hidden_size, n_layers)
    def forward(self, word_inputs, hidden,lang="insta"):
        seq_len = len(word_inputs)
        embedded = self.embedding(word_inputs).view(seq_len, 1, -1)
        size = embedded.size
        output, hidden = self.gru(embedded, hidden)

        return output, hidden, size

    def init_hidden(self):
        hidden = Variable(torch.zeros(self.n_layers, 1, self.hidden_size))
        hidden = hidden.cuda()
        return hidden