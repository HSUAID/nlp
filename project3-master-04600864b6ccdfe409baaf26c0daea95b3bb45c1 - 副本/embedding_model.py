#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import nltk
class embedding_model(object):
    
    def __init__(self):
        self.word_vect_dic = {}
        self.init_emb_model()
        
    def init_emb_model(self):
        with open('./data/glove.6B.100d.txt','r',encoding='utf-8') as fp:
            for line in fp:
                vars = line.split()
                self.word_vect_dic[vars[0]] = np.asarray(vars[1:], dtype='float16')
        fp.close()    
        
    def sent_vet_get(self,review_line):
        line_list = nltk.word_tokenize(review_line)
        line_vector = np.zeros((100))
#         line_vector = []
        len_n = len(line_list)
        if line_list == None or len_n == 0:
            return line_vector
        for word in line_list:
#             try:
#                 line_vector.append(self.word_vect_dic[word])
            if word in self.word_vect_dic:
                line_vector += self.word_vect_dic[word]
#             except KeyError:
            else:
                len_n = len_n - 1
            if len_n <= 0:
                len_n = 1
        return line_vector/len_n
#         word_vector = np.sum(line_vector,axis=0)
#         return np.array(word_vector)

