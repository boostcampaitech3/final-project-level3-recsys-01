#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import json 

import matplotlib.pyplot as plt
from matplotlib_venn import venn2


# In[ ]:


raw_data = pd.read_csv("./raw_data.csv", index_col=0)


# In[ ]:


raw_data.head()


# In[ ]:


raw_data.info()


# In[ ]:


# 사는 사람보다 판 사람이 더 많다
raw_data[['purchasing_user_profile_id', 'selling_user_profile_id']].nunique()


# In[ ]:


# 팔기만 하는 사람도 존재하고, 사기만 하는 사람도 존재한다
purchased = set(raw_data['purchasing_user_profile_id'])
sell = set(raw_data['selling_user_profile_id'])
# len(purchased.difference(sell))
# len(purchased.intersection(sell))
# len(sell.difference(purchased))

venn2(subsets=(len(purchased.difference(sell)), len(sell.difference(purchased)), len(purchased.intersection(sell))),
        set_labels = ('purchaser', 'seller'))
plt.show()


# In[ ]:


userid = list(purchased.union(sell))
userid_df = pd.DataFrame(
    {'userid': userid}
)
userid_dict = userid_df.to_dict()['userid']
# print(userid_dict)
with open('./userid.json', 'w') as outfile:
    json.dump(userid_dict, outfile, indent = 4) 


# In[ ]:


itemid_df = raw_data[['nifty_obj_contract_address', 'nifty_obj_token_id']].drop_duplicates().reset_index(drop=True)
itemid_dict = itemid_df.T.to_dict('list')
# print(itemid_dict)
with open('./itemid.json', 'w') as outfile:
    json.dump(itemid_dict, outfile, indent = 4)


# In[ ]:


# 데이터 전처리
new_data = raw_data.copy()
for x in new_data.columns:
    if new_data[x].dtype == 'object':
        new_data[x] = [s.strip() if not s is np.nan else s for s in new_data[x]]
new_data = new_data.dropna(subset=['nifty_obj_img_url'], axis=0)
new_data['nifty_obj_img_url'] = [x if x.startswith('http') else np.nan for x in new_data['nifty_obj_img_url']]
new_data = new_data.dropna(subset=['nifty_obj_img_url'], axis=0)
new_data.reset_index(drop=True, inplace=True)


# In[ ]:


# 데이터 export
new_data.to_csv('./preprocessed_data.csv', index=False)

