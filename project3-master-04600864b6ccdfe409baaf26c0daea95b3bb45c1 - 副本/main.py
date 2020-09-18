import time
from business import Business
from business_database import Business_database
def get_review_summary_for_business(biz_id):
# 	获取每一个business的评论总结
	return business.aspect_based_summary(biz_id)

def main(): 

    biz_ids = ['3dK3PIfmu09FFGi21QYPaA','S1N5-ZXwR4fUIPs6dLnBYQ','tstimHoMcYbkSC4eBA1wEg','QH2OSulslnQ7Yn8Xs81SPg','OoKNxTMu5YAaNgQKQ4SrzA','KWywu2tTEPWmR9JnBc0WyQ'] 
    # 指定几个business ids
    for biz_id in biz_ids:
        start = time.time()        
        aspect_summary = get_review_summary_for_business(biz_id)
        
        print("############################next biz_id summary##################################")
        
        normal_print_list = ["business_id","business_name","business_rating", "rating"]
        
        for item in aspect_summary.items():
        
            if item[0] in normal_print_list:
                print(str(item[0]) + ':' + str(item[1]))
            else:
#                 print(str('rating') + ':' + str(item[0]['rating']))
                for item_1 in item[1].items():
                    print("--------------------aspect:  " + str(item_1[0]) + "-------------------------")    
                    print(str('rating') + ':' + str(item_1[1]['rating']))
#                     print(str(item_1[1]['rating']) + ':' + str(data[1]))
                    for data in item_1[1].items():
                        if data[0] not in normal_print_list:
                            print('    ')
                            print('$$$$$$$$$$$$$$$$$$$$$' + str(data[0]) + '$$$$$$$$$$$$$$$$:')    
                            for line in data[1]:
                                print(line)
                            
                
                

if __name__ == "__main__":
	database = Business_database()
	business = Business(database)
	main()
