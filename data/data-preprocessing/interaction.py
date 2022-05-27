#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import json 


# ## 데이터 import (preprocessed_data.csv, userid.json, itmeid.json)

# In[2]:


with open('./userid.json') as json_file:
    userid = json.load(json_file)
    userid = {v: k for k, v in userid.items()}

with open('./itemid.json') as json_file:
    itemid = json.load(json_file)
    itemid = {v: k for k, v in itemid.items()}


# In[3]:


preprocessed_data = pd.read_csv('./preprocessed_data.csv')


# In[4]:


preprocessed_data['userid'] = [int(userid[idx]) for idx in preprocessed_data['purchasing_user_profile_id']]
preprocessed_data['itemid'] = [int(itemid[idx]) for idx in preprocessed_data['img_url']]


# In[5]:


preprocessed_data.info()


# ## Interaction data 생성

# In[12]:


MIN_INTERACTION = 30

agg_on_user = preprocessed_data.groupby("userid").agg({
    "itemid": "nunique"
})

active_user = agg_on_user[agg_on_user.itemid >= MIN_INTERACTION].index.values
active_df = preprocessed_data[preprocessed_data.userid.isin(active_user)]


# In[13]:


interaction = pd.pivot_table(active_df, 
                             index=["userid"], 
                             columns=["itemid"], 
                             values=["img_url"], 
                             aggfunc=["nunique"],
                             fill_value=0)
interaction.columns = np.arange(active_df.itemid.nunique())
interaction.reset_index(inplace=True, drop=True)
interaction


# In[14]:


sparsity = (interaction.to_numpy() == 0).mean()
sparsity, int(sparsity * 10000)


# In[15]:


interaction.to_csv(f"./interaction_min{MIN_INTERACTION}_sparse{int(sparsity * 10000)}.csv", 
                   index=False)


# ## Intraction과 관련된 json file들 저장

# In[10]:


def save_interaction_ids(df, id_name):
    interaction_id_dic = pd.DataFrame(
        {id_name: sorted(df[id_name].unique())}
    ).to_dict()[id_name]
    
    save_json(f"interaction_{id_name}", interaction_id_dic)

def save_json(fname, dic_data):
    with open(f"./{fname}_min{MIN_INTERACTION}.json", "w") as outfile:
        json.dump(dic_data, outfile, indent=4)


# In[16]:


itemid_imageurl = active_df[['itemid', 'nifty_obj_img_url']]
itemid_imageurl = itemid_imageurl.drop_duplicates(subset=["itemid"])
itemid_imageurl.set_index('itemid', inplace=True)
itemid_imageurl = itemid_imageurl.to_dict()['nifty_obj_img_url']

save_json("interaction_itemid_imageurl", itemid_imageurl)
save_interaction_ids(active_df, "userid")
save_interaction_ids(active_df, "itemid")


# In[ ]:




