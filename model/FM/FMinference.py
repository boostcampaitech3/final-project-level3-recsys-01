#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import json
import os.path

import joblib
from scipy import sparse

from lightfm.evaluation import recall_at_k


# In[2]:


# Data Import
transaction_data = pd.read_csv("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/transaction_data_min30.csv")
itemid_imageurl_json = pd.read_json("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/transaction_itemid_imageurl_min30.json", orient='records')
itemid_json = pd.read_json("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/transaction_itemid_min30.json", orient='records')
userid_json = pd.read_json("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/transaction_userid_min30.json", orient='records')


# In[3]:


itemid_imageurl_dict = itemid_imageurl_json.set_index('itemid').to_dict()['img_url']
itemid_dict = itemid_json.set_index('itemid').to_dict()['index']
userid_dict = userid_json.set_index('userid').to_dict()['index']


# In[4]:


transaction_data['userid_json'] = [int(userid_dict[idx]) for idx in transaction_data['userid']]
transaction_data['itemid_json'] = [int(itemid_dict[idx]) for idx in transaction_data['itemid']]


# In[5]:


transaction_data["rating"] = 1
ratings_df = transaction_data[["userid_json", "itemid_json", "rating"]]

df = ratings_df.copy()
users = df["userid_json"]
items = df["itemid_json"]

coo_shape = (len(users.unique()), len(items.unique()))

ratings_coo = sparse.coo_matrix((df["rating"], (users, items)), shape=coo_shape, dtype = np.int32)
print("ratings dataframe shape:", ratings_coo.shape)


# In[6]:


model_wo_item_feature = joblib.load("/opt/ml/final-project-level3-recsys-01/model/FM/FMmodel/FM_best_model.pkl") 

ratings_recall = recall_at_k(model_wo_item_feature,
                            ratings_coo,
                            k = 10).mean()
print("Loaded FM best model where recall@10 is", ratings_recall)


# In[7]:


def proceed_inference(inference_num = 10):

    INFERENCE_NUM = inference_num

    ratings_array = ratings_coo.toarray()

    predict_item_ids = np.where(ratings_array[INFERENCE_USERID] == 0)[0]
    predict_userids = np.full((len(predict_item_ids)), INFERENCE_USERID)
    prediction = model_wo_item_feature.predict(predict_userids, predict_item_ids)

    idx = sorted(range(len(prediction)), reverse=True, key=lambda k: prediction[k])

    result = {}
    itemid_dict = itemid_json.set_index('index').to_dict()['itemid']
    idx_num = 0

    while len(result) < INFERENCE_NUM:
        recommended_item = itemid_dict[predict_item_ids[idx[idx_num]]]
        recommended_image = itemid_imageurl_dict[recommended_item]
        recommended_df = transaction_data[transaction_data.img_url == recommended_image]
        recommended_image_url = list(recommended_df['nifty_obj_img_url'])[0]
        url = []
        cand_df = recommended_df[['nifty_obj_contract_address', 'nifty_obj_token_id']].drop_duplicates().reset_index(drop=True)
        cand_nifty_obj_contract_address = list(cand_df.nifty_obj_contract_address)
        cand_nifty_obj_token_id = list(cand_df.nifty_obj_token_id)
        cand_url = [str(cand_nifty_obj_contract_address[i])+'/'+str(cand_nifty_obj_token_id[i]) for i in range(cand_df.shape[0])]
        for x in cand_url:
            nft_url = "https://niftygateway.com/marketplace/item/"+x
            if True:
                url.append(nft_url)
        if url:
            result[recommended_image_url] = url
        idx_num += 1
    
    output = {'user_id': INFERENCE_USER_URL, 'recommendation': result}

    with open(f"/opt/ml/final-project-level3-recsys-01/model/FM/FMinference/output_{INFERENCE_USER_URL}.json", "w") as outfile:
        json.dump(output, outfile)
    print(f"Recommended items for {INFERENCE_USER_URL} saved as output_{INFERENCE_USER_URL}.json")
    print("Inference for", INFERENCE_USER_URL, "terminated")


# In[8]:


while True:
    INFERENCE_USER_URL = str(input("Enter USER_URL that needs to be inferenced...     "))
    user_info = pd.read_json("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/userid.json", orient='records')
    user_info = user_info.set_index('user_profile_profile_url').to_dict()['index']
    try:
        INFERENCE_USERID = user_info[INFERENCE_USER_URL]        
        print("Start inferencing for", INFERENCE_USER_URL, "...")
        break
    except:
        print("There is no certain USER_URL")
        print("Enter the correct USER_URL again")

file_exists = os.path.exists("/opt/ml/final-project-level3-recsys-01/model/FM/FMinference/output_"+INFERENCE_USER_URL+".json")

if not file_exists:
    try:
        INFERENCE_USERID = userid_dict[INFERENCE_USERID]
        proceed_inference()
    except:
        print("Not enough transaction data to infer for", INFERENCE_USER_URL, "...")
else:
    print(f"Recommended items for {INFERENCE_USER_URL} already saved as output_{INFERENCE_USER_URL}.json")

