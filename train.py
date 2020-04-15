import argparse
import etl
import helpers
import random
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import math
from attention_decoder import AttentionDecoderRNN
from encoder import EncoderRNN
import language
import os

language = 'insta_hashtag'
helpers.validate - language(language)

teacher_forcing_ratio = 0.5
clip = 5
device = torch.device('cuda:0')

def train(input_var, target_var, encode, decoder, encoder_opt, decoder_opt, criterion):
    encoder_opt.zero_grad()
    decoder_opt.zero_grad()
    loss = 0

    target_length = target_var.size()[0]

    encoder_hidden = encoder.init_hidden()
    encoder_outputs, encoder_hidden, size = encoder(input_var, encoder_hidden)
    print(size)

    decoder_input = Variable(torch.LongTensor([0]))
    decoder_input = decoder_input.cuda()
    decoder_context = Variable(torch.zeros(1, decoder.hidden_size))
    decoder_context = decoder_context.cuda()
    decoder_hidden = encoder_hidden

    use_teacher_forcing = random.random() < teacher_forcing_ratio
    if use_teacher_forcing:
        for di in range(target_length):
            decoder_output, decoder_context, decoder_hidden, decoder_attention = decoder(decoder_input,
                                                                                         decoder_context,
                                                                                         decoder_hidden,
                                                                                         encoder_outputs)
            loss += criterion(decoder_output, target_var[di])
            decoder_input = target_var[di]
    else:
        # Use previous prediction as next input
        for di in range(target_length):
            decoder_output, decoder_context, decoder_hidden, decoder_attention = decoder(decoder_input,
                                                                                         decoder_context,
                                                                                         decoder_hidden,
                                                                                         encoder_outputs)

            loss += criterion(decoder_output, target_var[di])

            topv, topi = decoder_output.data.topk(1)
            ni = topi[0][0]

            decoder_input = Variable(torch.cuda.LongTensor([[ni]]))
            decoder_input = decoder_input.cuda()

            if ni == 1:
                break

    loss.backward()
    torch.nn.utils.clip_grad_norm(encoder.parameters(), clip)
    torch.nn.utils.clip_grad_norm(encoder.parameters(), clip)
    encoder_opt.step()
    decoder_opt.step()

    return loss.data / target_length


input_lang, output_lang, pairs = etl.prepare_data
hidden_size = 500
n_layers = 2
dropout_p = 0.1

encoder = EncoderRNN(input_lang.n_word, hidden_size, n_layers)
decoder = AttentionDecoderRNN( hidden_size, output_lang.n_words, n_layers, dropout_p=dropout_p)

encoder = encoder.to(device)
decoder = decoder.to(device)

learning_rate = 0.0001
encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
decoder_optimizer = optim.Adam(decoder.patameters(), lr=learning_rate)

criterion = nn.NLLLoss()

n_epochs = 100000
plot_every = 20
print_every = 10

# path = "checkpoint/"+"params_epoch_{}.tar".format(54900)
# checkpoint = torch.load(path)
# encoder.load_state_dict(checkpoint['encoder'])
# decoder.load_state_dict(checkpoint['decoder'])
# decoder.attention.load_state_dict(checkpoint['decoder.attention'])
# epoch = checkpoint['epoch'] + 1  # load model
# encoder_optimizer.load_state_dict(checkpoint['encoder_optim'])
# decoder_optimizer.load_state_dict(checkpoint['decoder_optim'])

start = time.time()
plot_losses = []
print_loss_total = 0
plot_loss_total = 0

for epoch in range(0, n_epochs + 1):
    training_pair = etl.variables_from_pair(random.choice(pairs), input_lang, output_lang)
    input_variable = training_pair[0]
    target_variable = training_pair[1]

    loss = train(input_variable, target_variable, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion,
                 device)
    print_loss_total += loss
    plot_loss_total += loss

    if epoch % print_every == 0:
        print_loss_avg = print_loss_total / print_every
        print_loss_total = 0
        time_since = helpers.time_since(start, epoch / n_epochs)
        print('%s (%d %d%%) %.4f' % (time_since, epoch, epoch / n_epochs * 100, print_loss_avg))

    if epoch % 100 == 0:
        model_out_path = "checkpoint/" + "params_epoch_{}.tar".format(epoch)
        if not os.path.exists("checkpoint/"):
            os.makedirs("checkpoint/")
        print("세이브 시작")
        torch.save({
            'epoch': epoch,
            'encoder': encoder.state_dict(),
            'decoder': decoder.state_dict(),
            'encoder_optim': encoder_optimizer.state_dict(),
            'decoder_optim': decoder_optimizer.state_dict(),
            'decoder.attention': decoder.attention.state_dict()
        }, model_out_path)
        print("세이브 끝")

helpers.show_plot(plot_losses)