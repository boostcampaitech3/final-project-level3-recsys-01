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


new_data.columns


# In[9]:


user_colnames = ['user_profile_id', 'user_profile_profile_url', 'user_profile_name']
df1 = new_data[['purchasing_user_profile_id', 'purchasing_user_profile_profile_url', 'purchasing_user_profile_name']]
df2 = new_data[['selling_user_profile_id', 'selling_user_profile_profile_url', 'selling_user_profile_name']]
df1.columns = df2.columns = user_colnames
user_info = df1.append(df2)
user_info = user_info.drop_duplicates('user_profile_id')
user_info.reset_index(drop=True, inplace=True)


# In[10]:


userid_df = pd.DataFrame(
    {
        'user_profile_id': user_info.user_profile_id,
        'user_profile_profile_url': user_info.user_profile_profile_url,
        'user_profile_name': user_info.user_profile_name
    }
)
userid_df = userid_df.rename_axis('index').reset_index()
userid_df_dic = userid_df.to_json(orient="records")

with open(f"./userid.json", "w") as outfile:
    parsed = json.loads(userid_df_dic)
    json.dump(parsed, outfile, indent=4)


# In[11]:


itemid_df = pd.DataFrame(
    {'itemid': list(new_data['img_url'].unique())}
)
itemid_df = itemid_df.rename_axis('index').reset_index()
itemid_df_dic = itemid_df.to_json(orient="records")

with open(f"./itemid.json", "w") as outfile:
    parsed = json.loads(itemid_df_dic)
    json.dump(parsed, outfile, indent=4)


# In[12]:


# 데이터 export
new_data.to_csv('./preprocessed_data.csv', index=False)


# In[ ]:




