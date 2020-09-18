import nltk
import json
from business_database import Business_database
from sentimental_mode import sentimental_mode
# class Business_data_item(object):

# 	def __init__(self,business_id,name,stars):
# 		self.business_id = business_id
# 		self.name = name
# 		self.stars = stars

# class Review_data_item(object):

# 	def __init__(self,review_id,business_id,stars,text):
# 		self.review_id = review_id
# 		self.business_id = business_id
# 		self.stars = stars
# 		self.text = text

class Business(object):
# 	"""
# 	用来表示跟business相关的变量和函数
# 	"""

    # SENTIMENT_MODEL = SentimentModel() # 把已经训练好的模型存放在文件里，并导入进来


    def __init__(self,Database):
        self.database = Database
        self.sentimental_mode = sentimental_mode()
    def extract_aspects(self,business_id):
        """
        从一个business的review中抽取aspects
        """
        aspect_dic = {}
        aspect_phase = ''
        extracted_aspect = {}
        aspects_filter = ['time']
        if business_id not in self.database.review_dic:
            print('business_id not in review_dic')
            return
        review_list = self.database.review_dic[business_id]
        for review_item in review_list:
            review_sentence = review_item.text
            
#             print(review_sentence)
            if review_sentence == None or review_sentence.strip() == '':
                continue
            # 分词
            tokens = nltk.word_tokenize(review_sentence)
            # 词性标注
            tagged = nltk.pos_tag(tokens)
            
            for index,tuple_data in enumerate(tagged):
                if (tuple_data[1] == 'NN' or tuple_data[1] == 'NNP' or tuple_data[1] == 'NNS') and index + 1 != len(tagged):
                    if aspect_phase == '':
                        aspect_phase = tuple_data[0]
                    else:   
                        aspect_phase = aspect_phase + ' ' + tuple_data[0]
                else:
                    if aspect_phase not in aspect_dic:
                        aspect_dic[aspect_phase] = []
                        aspect_dic[aspect_phase].append(review_item)
                    elif aspect_phase != '':
                        aspect_dic[aspect_phase].append(review_item)# = aspect_dic[aspect_phase] + 1
                    aspect_phase = ''
                    
        aspect_dic = sorted(aspect_dic.items(), key=lambda item: len(item[1]), reverse=True)
#         print(aspect_dic)+++++
        for aspect_dic_item in aspect_dic:
            if len(extracted_aspect) < 5:
                if aspect_dic_item[0] not in aspects_filter:
                    extracted_aspect[aspect_dic_item[0]] = aspect_dic_item[1]
            else:
                break
        return extracted_aspect

    def aspect_based_summary(self,business_id):
        """
        返回一个business的summary. 针对于每一个aspect计算出它的正面负面情感以及TOP reviews. 
        具体细节请看给定的文档。 
        """

        aspects_dic = self.extract_aspects(business_id)
        business_name = self.database.business_dic[business_id].name
        pos_aspect_dic = {}
        neg_aspect_dic = {}
        review_segment_dic = {}     
        
        for aspect,review_list in aspects_dic.items():
            for review in review_list:
                review_sen = review.text
                if review_sen == None or review_sen.split() == '':
                    continue
                segment_sen = self.get_segment(review_sen,aspect,aspects_dic)
#                 print(segment_sen)
                if len(str.split(segment_sen)) > len(str.split(aspect)) + 1:
                    score = self.sentimental_mode.predic_prob(segment_sen)
#                     print(score)
#                     print(aspect)
                    key = aspect + '_' + review.review_id
                    if score > 0.5:
                        if aspect not in pos_aspect_dic:
                            pos_aspect_dic[aspect] = []
                        pos_aspect_dic[aspect].append([score,key])
                    else:
                        if aspect not in neg_aspect_dic:
                            neg_aspect_dic[aspect] = []
                        neg_aspect_dic[aspect].append([score,key])     
                    
                    review_segment_dic[key] = review.text
#         print(pos_aspect_dic) 
        
        aspects_summary = {}
        for aspect,review_list in aspects_dic.items():
            if aspect not in aspects_summary:
                aspects_summary[aspect] = {}
            #aspect pos 
            pos_score = 0
            pos_aspect_dic[aspect].sort(key=lambda x:x[0],reverse = True)   
            aspects_summary[aspect]['pos_reviews'] = []
            pos_index = 0
            for index,list in enumerate(pos_aspect_dic[aspect]):
                pos_score += list[0]          
                if review_segment_dic[list[1]] not in aspects_summary[aspect]['pos_reviews'] and pos_index < 5:
                    aspects_summary[aspect]['pos_reviews'].append(review_segment_dic[list[1]])
                    pos_index += 1
            #aspect neg                
            neg_score = 0
            neg_aspect_dic[aspect].sort(key=lambda x:x[0],reverse = False)   
            aspects_summary[aspect]['neg_reviews'] = []
            neg_index = 0
            for index,list in enumerate(neg_aspect_dic[aspect]):
                neg_score += list[0]
                if review_segment_dic[list[1]] not in aspects_summary[aspect]['neg_reviews'] and neg_index < 5:
#                     if neg_index > 5:
#                         break
                    aspects_summary[aspect]['neg_reviews'].append(review_segment_dic[list[1]])
                    neg_index += 1
#                 if neg_index < 5:
#                     aspects_summary[aspect]['neg_reviews'].append(review_segment_dic[list[1]])
#                 neg_index +=1
#                 neg_score += list[0]
                
            aspects_summary[aspect]['rating'] = ((pos_score + neg_score)/len(pos_aspect_dic[aspect] + neg_aspect_dic[aspect]))*5   
        all_aspects_rating = 0
        for item in aspects_summary.items():
#             print(item[1]['rating'])
            all_aspects_rating += item[1]['rating']
        business_rating = all_aspects_rating/len(aspects_summary)
        return {'business_id':business_id,
                'business_name':business_name,
                'business_rating':business_rating,
                'aspects_summary':aspects_summary
                }
        
    def get_segment(self,review_sentence,aspect,aspect_dic):
        first_flag = 0
        segment_aspect_list = []
        segment_tag_list = []
        stop_punct_map = {c: None for c in ',.!?;'}
        if aspect not in review_sentence or aspect not in review_sentence:
            print('Error aspect not in review_sentence or aspect not in review_sentence')
            return review_sentence
        
        #如果句子只包括一个aspect 不分段截取句子
        # 分词
        tokens = nltk.word_tokenize(review_sentence)
        del_list = []
        if len(aspect.split()) > 1:
            for idx,token in enumerate(tokens):
#                 print(token)
#                 print('sssssssssssss')
                if token in aspect:
                    del_list.append(token)
#                     print(del_list)        
                    if first_flag == 0:
                        insert_index = idx
                    first_flag = 1
            tokens.insert(insert_index,aspect)            
            for del_token in del_list:
                tokens.remove(del_token)
        # 词性标注
        tagged = nltk.pos_tag(tokens)        
        get_segment_aspect_list = []
        #如果只有一个aspect return自己
        for index,tuple_data in enumerate(tagged):
            segment_tag_list.append(tuple_data[1])
            if (tuple_data[1] == 'NN' or tuple_data[1] == 'NNP' or tuple_data[1] == 'NNS') and tuple_data[0] in aspect_dic:
                segment_aspect_list.append(index)
                if tuple_data[0] == aspect:
                    get_segment_aspect_list.append(index)
#                if tag == "JJ" or tag == "ADJ":             
        if len(segment_aspect_list) == 1:
            return review_sentence
#         print(segment_aspect_list)
#         print(segment_tag_list)
        if len(segment_aspect_list) == 0:
            print('segment_aspect_list shouldnt be none ')
            
        segment_left_index = 0
        segment_aspect_index = get_segment_aspect_list[0]
        segment_right_index = len(tokens) - 1
#         print(segment_aspect_list)
        if segment_aspect_list.index(segment_aspect_index) > 0:
            segment_left_index = segment_aspect_list[segment_aspect_list.index(segment_aspect_index) - 1] + 1
        if segment_aspect_list.index(segment_aspect_index) < len(segment_aspect_list) - 1:
            segment_right_index = segment_aspect_list[segment_aspect_list.index(segment_aspect_index) + 1] - 1
            
        #如果右边有aspect，则截取本aspect和右边aspect之间的段落    
        if segment_right_index != len(tokens) - 1:
        
            for index,token in enumerate(tokens[segment_aspect_index:segment_right_index+1]):
                if token in stop_punct_map:
#                     print(index)
#                     print(token)
#                     print(segment_aspect_index)
                    segment_right_index = segment_aspect_index + index - 1
                    break
                    
            if segment_right_index == segment_aspect_list[segment_aspect_list.index(segment_aspect_index) + 1] - 1:
                for index,token in enumerate(segment_tag_list[segment_aspect_index:segment_right_index+1]):
                    if token == "JJ" or token == "ADJ":  
                        segment_right_index = segment_aspect_index + index
                        break              
                        
        #如果左边有aspect，则截取本aspect和左边aspect之间的段落    
        if segment_left_index != 0:          
            for index,token in enumerate(reversed(tokens[segment_left_index:segment_aspect_index+1])):
                if token in stop_punct_map:
                    segment_left_index = segment_aspect_index - index + 1
                    break
                    
            if segment_left_index == segment_aspect_list[segment_aspect_list.index(segment_aspect_index) - 1] + 1:
                for index,token in enumerate(reversed(tokens[segment_left_index:segment_aspect_index+1])):
                    if index > 2:
                        break
                    elif token == "JJ" or token == "ADJ" or token == 'JJR' or token == 'JJS':  
                        segment_left_index = segment_aspect_index - index
                        break         
        #为了debug打印的信息
        if segment_left_index < 0 or segment_right_index > len(tokens) - 1 or segment_left_index > segment_right_index:
            print('Error')
            print(review_sentence)
            print(aspect)
            print('###############################')
            print(segment_left_index)
            print(segment_right_index)
#         " ".join(list[segment_left_index:segment_right_index+1])
        return " ".join(tokens[segment_left_index:segment_right_index+1])
                            