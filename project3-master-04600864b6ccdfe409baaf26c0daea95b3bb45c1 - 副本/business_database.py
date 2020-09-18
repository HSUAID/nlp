import json
class Business_data_item(object):

	def __init__(self,business_id,name,stars):
		self.business_id = business_id
		self.name = name
		self.stars = stars

class Review_data_item(object):

	def __init__(self,review_id,business_id,stars,text,user_id):
		self.review_id = review_id
		self.business_id = business_id
		self.stars = stars
		self.text = text
		self.user_id = user_id
        
class Business_database(object):
	"""
	用来表示跟business相关的变量和函数
	"""

	# SENTIMENT_MODEL = SentimentModel() # 把已经训练好的模型存放在文件里，并导入进来
	

	def __init__(self):
		# 初始化变量以及函数
#         print("step2 读取数据开始==================")        
		self.business_dic = {}
		self.review_dic = {}
		self.user_rating_dic = {}
		self.read_data()
#         self.user_rating_get()

	def	read_data(self):
#         print(debug)
		with open('./data/business.json','r',encoding='utf-8') as fp:
			for line in fp:
				line_data = json.loads(line)
				business_id = line_data["business_id"]
				business_name = line_data["name"]
				review_count = line_data["review_count"] 
#                 print(review_count)
				business_stars = line_data["stars"]                      
				if review_count >= 100:
#                     print('11111')
					self.review_dic[business_id] = []
					Business_item = Business_data_item(business_id,business_name,business_stars)
					self.business_dic[business_id] = Business_item

		with open('./data/review.json', 'r',encoding='utf-8') as fp:
			for line in fp:
				line_data = json.loads(line)
				review_id = line_data['review_id']
				business_id = line_data['business_id']
				review_stars = line_data['stars']
				review_text = line_data['text']
				user_id = line_data['user_id']
				if business_id in self.business_dic:
					Review_item = Review_data_item(review_id,business_id,review_stars,review_text,user_id)
					self.review_dic[business_id].append(Review_item)
#         for var in review_dic.values():
#             if var.user_id not in user_rating_average:
#                 self.user_rating_dic[var.user_id] = []
#                 self.user_rating_dic[var.user_id].append(var.stars)
#             else:
#                 self.user_rating_dic[var.user_id].append(var.stars)                 
                