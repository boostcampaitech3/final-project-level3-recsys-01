#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from tqdm import tqdm
import random
import json 


# ## 데이터 import (preprocessed_data.csv, userid.json, itmeid.json)

# In[7]:


itemid_json = pd.read_json("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/itemid.json", orient='records')
userid_json = pd.read_json("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/userid.json", orient='records')
itemid = itemid_json.set_index('itemid').to_dict()['index']
userid = userid_json.set_index('user_profile_id').to_dict()['index']


# In[8]:


preprocessed_data = pd.read_csv('./preprocessed_data.csv')


# In[9]:


preprocessed_data['userid'] = [int(userid[idx]) for idx in preprocessed_data['purchasing_user_profile_id']]
preprocessed_data['itemid'] = [int(itemid[idx]) for idx in preprocessed_data['img_url']]


# In[10]:


MIN_TRANSACTION = 30

agg_on_user = preprocessed_data.groupby("userid").agg({
    "itemid": "nunique"
})

active_user = agg_on_user[agg_on_user.itemid >= MIN_TRANSACTION].index.values
active_df = preprocessed_data[preprocessed_data.userid.isin(active_user)]

# userid itemid 기준으로 unique한 item만 남김
active_df.drop_duplicates(subset=['userid', 'itemid'], inplace=True)

# userid와 nifty_obj_timestamp를 기준으로 정렬
active_df = active_df.sort_values(['userid', 'nifty_obj_timestamp'])
active_df.reset_index(drop=True, inplace=True)

# 실제 모델에 사용할 학습 데이터
active_df.to_csv(f"transaction_data_min{MIN_TRANSACTION}.csv", index=False)


# In[11]:


label = []
OPTIMAL_SEED = 149
RECALL_K = 10

for x in list(active_df.userid.unique()):
    n = active_df[active_df['userid'] == x].shape[0]
    temp = ['train'] * n
    random.seed(OPTIMAL_SEED)
    five = random.sample(list(range(n)), RECALL_K)
    for y in five:
        temp[y] = 'test'
    label.extend(temp)

assert active_df.shape[0] == len(label)
active_df['label'] = label

train = active_df[active_df['label'] == 'train']
test = active_df[active_df['label'] == 'test']

train = active_df[active_df['label'] == 'train']
train.reset_index(drop=True, inplace=True)
train.to_csv(f"./train{RECALL_K}_min{MIN_TRANSACTION}.csv", index=False)

test = active_df[active_df['label'] == 'test']
test.reset_index(drop=True, inplace=True)
test.to_csv(f"./test{RECALL_K}_min{MIN_TRANSACTION}.csv", index=False)
assert active_df.purchasing_user_profile_id.nunique()*RECALL_K == test.shape[0]

test_answer = test.sort_values(['userid', 'itemid'])[['userid', 'itemid']]
test_answer.to_csv(f"./test{RECALL_K}_answer_min{MIN_TRANSACTION}.csv", index=False)

assert len(train.userid.unique()) == len(test.userid.unique())
print('전체 데이터의 item 개수: ', len(set(active_df.itemid)), '개')
print('train에 존재하지 않는 test의 item 개수: ', len(set(train.itemid)), '중의', len(set(test.itemid).difference(set(train.itemid))), '개')


# In[12]:


def save_transaction_ids(df, id_name):
    transaction_id = pd.DataFrame(
        {id_name: sorted(df[id_name].unique())}
    )
    transaction_id = transaction_id.rename_axis('index').reset_index()
    transaction_id_dic = transaction_id.to_json(orient="records")
    save_json(f"transaction_{id_name}", transaction_id_dic)

def save_json(fname, dic_data):

    with open(f"./{fname}_min{MIN_TRANSACTION}.json", "w") as outfile:
        parsed = json.loads(dic_data)
        json.dump(parsed, outfile, indent=4)


# In[13]:


itemid_imageurl = active_df[['itemid', 'nifty_obj_img_url']]
itemid_imageurl = itemid_imageurl.drop_duplicates(subset=["itemid"])
itemid_imageurl = itemid_imageurl.to_json(orient="records")

save_json("transaction_itemid_imageurl", itemid_imageurl)
save_transaction_ids(active_df, "userid")
save_transaction_ids(active_df, "itemid")


# In[ ]:




