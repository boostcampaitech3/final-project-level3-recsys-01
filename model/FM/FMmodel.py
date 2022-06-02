#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import joblib

from scipy import sparse

from lightfm import LightFM
from lightfm.evaluation import recall_at_k


# In[2]:


# Data Import
ratings_df = pd.read_csv("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/transaction_data_min30.csv")
itemid_imageurl_json = pd.read_json("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/transaction_itemid_imageurl_min30.json", orient='records')
itemid_json = pd.read_json("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/transaction_itemid_min30.json", orient='records')
userid_json = pd.read_json("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/transaction_userid_min30.json", orient='records')


# In[3]:


itemid_imageurl_dict = itemid_imageurl_json.set_index('itemid').to_dict()['img_url']
itemid_dict = itemid_json.set_index('itemid').to_dict()['index']
userid_dict = userid_json.set_index('userid').to_dict()['index']


# In[4]:


ratings_df['userid_json'] = [int(userid_dict[idx]) for idx in ratings_df['userid']]
ratings_df['itemid_json'] = [int(itemid_dict[idx]) for idx in ratings_df['itemid']]


# In[5]:


ratings_df["rating"] = 1
ratings_df = ratings_df[["userid_json", "itemid_json", "rating"]]

df = ratings_df.copy()
users = df["userid_json"]
items = df["itemid_json"]

coo_shape = (len(users.unique()), len(items.unique()))

ratings_coo = sparse.coo_matrix((df["rating"], (users, items)), shape=coo_shape, dtype = np.int32)
print("ratings dataframe shape:", ratings_coo.shape)


# In[6]:


MODEL = 'warp-kos'
NUM_COMPONENTS = 14
K = 26
N = 43
NUM_EPOCHS = 223
USER_ALPHA = 0.6738
LEARNING_RATE = 0.3865
LEARNING_SCHEDULE = 'adadelta'
RHO = 0.6694
EPSILON = 0.005253
MAX_SAMPLED = 99

# Define a new model instance
model = LightFM(loss=MODEL,
                random_state=42,
                user_alpha=USER_ALPHA,
                no_components=NUM_COMPONENTS,
                k=K,
                n=N,
                learning_rate=LEARNING_RATE,
                learning_schedule=LEARNING_SCHEDULE,
                rho=RHO,
                epsilon=EPSILON,
                max_sampled=MAX_SAMPLED)

model_wo_item_feature = model.fit(ratings_coo,
                epochs=NUM_EPOCHS,
                verbose = True)

ratings_recall = recall_at_k(model_wo_item_feature,
                    ratings_coo,
                    k = 10).mean()
print("FM best model recall@10: ", ratings_recall)

joblib.dump(model_wo_item_feature, "/opt/ml/final-project-level3-recsys-01/model/FM/FMmodel/FM_best_model.pkl")


# In[ ]:




