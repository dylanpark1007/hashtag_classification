import helpers
import torch
from language import Language
from torch.autograd import Variable
import random 
from konlpy.tag import Okt
from sklearn.model_selection import train_test_split
max_length = 20
    
def filter_pair(p):
    
    is_good_length = len(p[0].split(' ')) < max_length and len(p[1].split(' ')) < max_length
    return is_good_length

def filter_pairs(pairs):
    return [pair for pair in pairs if filter_pair(pair)]

def read_languages(lang):
   
   
    with open('./data/%s.txt' % lang,encoding='utf-8')as doc:
      doc =doc.read()
      lines = doc.strip().split('\n')
    
      # random.shuffle(lines)
      # if(usage =="train"):
      #   lines =lines[0:int(len(lines)*0.8)]
      # elif(usage =="test"):
      #   lines = lines[int(len(lines)*0.8):]
      pairs=[]
      for l in lines:
        k = [s for s in l.split('\t')]
        if len(k) == 2 :
          if k[0] == '' or k[1] == '':
            continue
          pairs.append(k) 

      input_lang = Language('insta')
      output_lang = Language(lang)
     
      return input_lang, output_lang, pairs

def prepare_data(lang_name, usage):

    input_lang, output_lang, pairs = read_languages(lang_name)
    pairs = filter_pairs(pairs)
    random.shuffle(pairs)

    # Index words
    for pair in pairs:
        input_lang.index_words(pair[0])
        output_lang.index_words(pair[1])
    # if usage=="train":
    #   pairs =pairs[0:int(len(pairs)*0.8)]    
    # elif usage =="test":
    #   pairs = pairs[int(len(pairs)*0.8):]
    return input_lang, output_lang, pairs,

def indexes_from_sentence(lang, sentence):
    sentence=' '.join(sentence)
    
    return [lang.word2index[word] for word in sentence.split(' ')]

def variable_from_sentence(lang, sentence):
    indexes = indexes_from_sentence(lang, sentence)
    var = Variable(torch.LongTensor(indexes).view(-1, 1))
    var = var.cuda()
    return var

def variables_from_pair(pair, input_lang, output_lang):
    input_variable = variable_from_sentence(input_lang, pair[0].split(" "))
    input_variable = input_variable.cuda()
    target_variable = variable_from_sentence(output_lang, pair[1].split(" "))
    target_variable = target_variable.cuda()
    return input_variable, target_variable