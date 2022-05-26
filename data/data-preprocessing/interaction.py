#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import json 
from tqdm import tqdm


# In[2]:


# 데이터 import
preprocessed_data = pd.read_csv('./preprocessed_data.csv')
with open('./userid.json') as json_file:
    userid = json.load(json_file)
    userid = {v: k for k, v in userid.items()}

with open('./itemid.json') as json_file:
    itemid = json.load(json_file)
    itemid = {str(v): k for k, v in itemid.items()}


# In[3]:


preprocessed_data['userid'] = [userid[preprocessed_data['purchasing_user_profile_id'][i]] for i in range(preprocessed_data.shape[0])]
preprocessed_data['itemid'] = [str([preprocessed_data['nifty_obj_contract_address'][i], preprocessed_data['nifty_obj_token_id'][i]]) for i in range(preprocessed_data.shape[0])]
preprocessed_data['itemid'] = [itemid[x] for x in preprocessed_data['itemid']]


# In[4]:


itemid_imageurl = preprocessed_data[['itemid', 'nifty_obj_img_url']]
itemid_imageurl.drop_duplicates(inplace=True)
itemid_imageurl.set_index('itemid', inplace=True)
itemid_imageurl = itemid_imageurl.to_dict()['nifty_obj_img_url']
# print(interaction_userid)
with open('./itemid_imageurl.json', 'w') as outfile:
    json.dump(itemid_imageurl, outfile, indent = 4) 


# In[ ]:


interaction_userid = pd.DataFrame(
    {'userid': sorted(preprocessed_data['userid'].unique())}
)
interaction_userid = interaction_userid.to_dict()['userid']
# print(interaction_userid)
with open('./interaction_userid.json', 'w') as outfile:
    json.dump(interaction_userid, outfile, indent = 4) 
with open('./interaction_userid.json') as json_file:
    interaction_userid = json.load(json_file)
    interaction_userid = {v: k for k, v in interaction_userid.items()}
preprocessed_data['userid'] = list(map(int, [interaction_userid[x] for x in preprocessed_data['userid']]))


# In[ ]:


interaction_itemid = pd.DataFrame(
    {'itemid': sorted(preprocessed_data['itemid'].unique())}
)
interaction_itemid = interaction_itemid.to_dict()['itemid']
# print(interaction_itemid)
with open('./interaction_itemid.json', 'w') as outfile:
    json.dump(interaction_itemid, outfile, indent = 4) 
with open('./interaction_itemid.json') as json_file:
    interaction_itemid = json.load(json_file)
    interaction_itemid = {v: k for k, v in interaction_itemid.items()}
preprocessed_data['itemid'] = list(map(int, [interaction_itemid[x] for x in preprocessed_data['itemid']]))


# In[ ]:


interaction = np.zeros((len(preprocessed_data['userid'].unique()),len(preprocessed_data['itemid'].unique())))
for i in tqdm(range(preprocessed_data.shape[0])):
    interaction[preprocessed_data['userid'][i]][preprocessed_data['itemid'][i]] = 1
interaction = pd.DataFrame(interaction)


# In[ ]:


interaction.to_csv("./interaction.csv", index=False)

