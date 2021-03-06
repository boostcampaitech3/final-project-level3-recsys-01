# -*- coding: utf-8 -*-
import requests
import pandas as pd

#data['results']==None 일때까지 page 늘리면서 data 빼오기

start_date = input('시작 날짜를 입력하세요: (예시: 2022-05-02) ')
end_date = input('마지막 날짜를 입력하세요: (예시: 2022-05-09) ')

total_page = 1760
url = 'https://api.niftygateway.com/market/all-data/?page={%22current%22:'+str(total_page)+',%22size%22:100}&filters={%22exclude_types%22:[%22withdrawals%22,%22primary_market_sales%22,%22single_nifty_offers%22,%22global_nifty_offers%22,%22attribute_nifty_offers%22,%22primary_market_bids%22,%22gifts%22,%22deposits%22,%22listings%22],%22date_start%22:%22'+start_date+'+00:00:00%22,%22date_end%22:%22'+end_date+'+23:59:59%22}'
while requests.get(url).json()['data']['results']!=[]:
    url = 'https://api.niftygateway.com/market/all-data/?page={%22current%22:'+str(total_page)+',%22size%22:100}&filters={%22exclude_types%22:[%22withdrawals%22,%22primary_market_sales%22,%22single_nifty_offers%22,%22global_nifty_offers%22,%22attribute_nifty_offers%22,%22primary_market_bids%22,%22gifts%22,%22deposits%22,%22listings%22],%22date_start%22:%22'+start_date+'+00:00:00%22,%22date_end%22:%22'+end_date+'+23:59:59%22}'
    total_page +=1
total_page-=2

print("total page : ",total_page)

def get_url(page):
    url_list = []
    for i in range(1,page):
        url = 'https://api.niftygateway.com/market/all-data/?page={%22current%22:'+str(i)+',%22size%22:100}&filters={%22exclude_types%22:[%22withdrawals%22,%22primary_market_sales%22,%22single_nifty_offers%22,%22global_nifty_offers%22,%22attribute_nifty_offers%22,%22primary_market_bids%22,%22gifts%22,%22deposits%22,%22listings%22],%22date_start%22:%22'+start_date+'+00:00:00%22,%22date_end%22:%22'+end_date+'+23:59:59%22}'
        url_list.append(url)
    return url_list

#sales 중 sale만 받아오기
url = 'https://api.niftygateway.com/market/all-data/?page={%22current%22:1,%22size%22:100}&filters={%22exclude_types%22:[%22withdrawals%22,%22primary_market_sales%22,%22single_nifty_offers%22,%22global_nifty_offers%22,%22attribute_nifty_offers%22,%22primary_market_bids%22,%22gifts%22,%22deposits%22,%22listings%22],%22date_start%22:%22'+start_date+'+00:00:00%22,%22date_end%22:%22'+end_date+'+23:59:59%22}'


url_list = get_url(total_page)

print('url list 생성 완료')

df = pd.DataFrame(columns={'selling_user_profile_id','selling_user_profile_name',
                    'selling_user_profile_profile_url','purchasing_user_profile_id',
                    'purchasing_user_profile_name','purchasing_user_profile_profile_url',
                    'nifty_obj_contract_address','nifty_obj_name',
                    'nifty_obj_img_url','nifty_obj_token_id','nifty_obj_made_user',
                    'nifty_obj_timestamp','nifty_obj_total_num_editions','nifty_obj_likes'
                    })
for j in range(1,total_page):
    data = requests.get(url_list[j-1]).json()
    if j%10==0:
        print(j)
    for i in range(100):
        if data['data']['results'][i]['SellingUserProfile'] != None:
            selling_user_profile = data['data']['results'][i]['SellingUserProfile']
            selling_user_profile_id = selling_user_profile['id']
            selling_user_profile_name = selling_user_profile['name']
            selling_user_profile_profile_url = selling_user_profile['profile_url']
            
            purchasing_user_profile = data['data']['results'][i]['PurchasingUserProfile']
            purchasing_user_profile_id = purchasing_user_profile['id']
            purchasing_user_profile_name = purchasing_user_profile['name']
            purchasing_user_profile_profile_url = purchasing_user_profile['profile_url']
            
            nifty_obj = data['data']['results'][i]['NiftyObject']
            nifty_obj_contract_address = nifty_obj['contractAddress']
            nifty_obj_name = nifty_obj['name']
            nifty_obj_img_url = nifty_obj['image_url']
            nifty_obj_token_id = nifty_obj['tokenId']
            nifty_obj_made_user = nifty_obj['unmintedNiftyObjThatCreatedThis']['contractObj']['userWhoCreated_id']
            nifty_obj_timestamp = nifty_obj['unmintedNiftyObjThatCreatedThis']['Timestamp']
            nifty_obj_total_num_editions = nifty_obj['unmintedNiftyObjThatCreatedThis']['niftyTotalNumOfEditions']
            nifty_obj_likes = nifty_obj['unmintedNiftyObjThatCreatedThis']['likes']
            new_data = {'selling_user_profile_id':selling_user_profile_id,
                    'selling_user_profile_name':selling_user_profile_name,
                    'selling_user_profile_profile_url':selling_user_profile_profile_url,
                    'purchasing_user_profile_id':purchasing_user_profile_id,
                    'purchasing_user_profile_name':purchasing_user_profile_name,
                    'purchasing_user_profile_profile_url':purchasing_user_profile_profile_url,
                    'nifty_obj_contract_address':nifty_obj_contract_address,
                    'nifty_obj_name':nifty_obj_name,
                    'nifty_obj_img_url':nifty_obj_img_url,
                    'nifty_obj_token_id':nifty_obj_token_id,
                    'nifty_obj_made_user':nifty_obj_made_user,
                    'nifty_obj_timestamp':nifty_obj_timestamp,
                    'nifty_obj_total_num_editions':nifty_obj_total_num_editions,
                    'nifty_obj_likes':nifty_obj_likes}
            df = df.append(new_data,ignore_index=True)                  


print(df)
print('dataframe 생성 완료')

# name = 'interaction_data_sale_{}_{}.csv'.format(start_date,end_date)
# df.to_csv(name)
# print('크롤링 완료')