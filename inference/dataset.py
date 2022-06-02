import numpy as np
import pandas as pd
import os
from scipy import sparse
import warnings
warnings.filterwarnings("ignore")


class Dataset:

    def __init__(self, data_dir: str, rating_fname="transaction_data_min30.csv") -> None:
        self.data_dir = data_dir
        self.rating_file = os.path.join(data_dir, rating_fname)
        
        self.transaction_data = pd.read_csv(self.rating_file)
        self.itemid_imageurl_json = pd.read_json(os.path.join(self.data_dir, "transaction_itemid_imageurl_min30.json"), orient='records')
        self.itemid_json = pd.read_json(os.path.join(self.data_dir, "transaction_itemid_min30.json"), orient='records')
        self.userid_json = pd.read_json(os.path.join(self.data_dir, "transaction_userid_min30.json"), orient='records')

        self.itemid_imageurl_dict = self.itemid_imageurl_json.set_index('itemid').to_dict()['img_url']
        self.itemid_dict = self.itemid_json.set_index('itemid').to_dict()['index']
        self.userid_dict = self.userid_json.set_index('userid').to_dict()['index']

        self.transaction_data['userid_json'] = [int(self.userid_dict[idx]) for idx in self.transaction_data['userid']]
        self.transaction_data['itemid_json'] = [int(self.itemid_dict[idx]) for idx in self.transaction_data['itemid']]

        self.transaction_data["rating"] = 1

        self.user_info = pd.read_json(os.path.join(self.data_dir, "userid.json"), orient='records')
        self.user_info = self.user_info.set_index('user_profile_profile_url').to_dict()['index']


class FMDataset:
    
    def __init__(self, transaction_data) -> None:
        
        self.transaction_data = transaction_data
        self.ratings_df = self.transaction_data[["userid_json", "itemid_json", "rating"]]
    
    def to_coo(self):
        df = self.ratings_df.copy()
        users = df["userid_json"]
        items = df["itemid_json"]

        coo_shape = (len(users.unique()), len(items.unique()))

        ratings_coo = sparse.coo_matrix((df["rating"], (users, items)), shape=coo_shape, dtype = np.int32)
        print("ratings dataframe shape:", ratings_coo.shape)
        return ratings_coo