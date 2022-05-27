#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from datetime import datetime
import json 

import matplotlib.pyplot as plt
from matplotlib_venn import venn2


# In[2]:


raw_data = pd.read_csv("./raw_data.csv", index_col=0)


# In[3]:


raw_data.head()


# In[4]:


raw_data.info()


# In[5]:


# 사는 사람보다 판 사람이 더 많다
raw_data[['purchasing_user_profile_id', 'selling_user_profile_id']].nunique()


# In[6]:


# 팔기만 하는 사람도 존재하고, 사기만 하는 사람도 존재한다
purchased = set(raw_data['purchasing_user_profile_id'])
sell = set(raw_data['selling_user_profile_id'])
# len(purchased.difference(sell))
# len(purchased.intersection(sell))
# len(sell.difference(purchased))

venn2(subsets=(len(purchased.difference(sell)), len(sell.difference(purchased)), len(purchased.intersection(sell))),
        set_labels = ('purchaser', 'seller'))
plt.show()


# In[7]:


# 데이터 전처리
new_data = raw_data.copy()
for x in new_data.columns:
    if new_data[x].dtype == 'object':
        new_data[x] = [s.strip() if not s is np.nan else s for s in new_data[x]]
new_data = new_data.dropna(subset=['nifty_obj_img_url'], axis=0)
new_data['nifty_obj_img_url'] = [x if x.startswith('http') else np.nan for x in new_data['nifty_obj_img_url']]
new_data = new_data.dropna(subset=['nifty_obj_img_url'], axis=0)
new_data['img_url'] = [x.split('/')[-1] for x in new_data['nifty_obj_img_url']]
new_data['extension'] = [x.split('.')[-1] if len(x.split('.')[-1]) < 10 else np.nan for x in new_data['img_url']]
new_data['nifty_obj_timestamp'] = [datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ') for x in new_data['nifty_obj_timestamp']]
new_data.reset_index(drop=True, inplace=True)


# In[8]:


userid = list(purchased.union(sell))
userid_df = pd.DataFrame(
    {'userid': userid}
)
userid_dict = userid_df.to_dict()['userid']
# print(userid_dict)
with open('./userid.json', 'w') as outfile:
    json.dump(userid_dict, outfile, indent = 4) 


# In[9]:


itemid_df = pd.DataFrame(
    {'itemid': list(new_data['img_url'].unique())}
)
itemid_dict = itemid_df.to_dict()['itemid']
# print(itemid_dict)
with open('./itemid.json', 'w') as outfile:
    json.dump(itemid_dict, outfile, indent = 4)


# In[10]:


# 데이터 export
new_data.to_csv('./preprocessed_data.csv', index=False)

