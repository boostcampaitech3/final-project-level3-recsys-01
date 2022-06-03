import pandas as pd


class TransactionData:
    def __init__(self, transaction_data_path="./data/transaction_data_min30.csv"):
        self.transaction_df = pd.read_csv(transaction_data_path)
        self.interaction_data = None
    
    def get_transaction_data(self):
        return self.transaction_df
    
    def get_interaction_data(self):
        self.interaction_data = pd.pivot_table(self.transaction_df,
                                              index=["userid"],
                                              columns=["itemid"],
                                              values=["img_url"],
                                              aggfunc=["nunique"],
                                              fill_value=0)
        self.interaction_data.columns = sorted(self.transaction_df.itemid.unique())
        self.interaction_data = self.interaction_data.reset_index(drop=True)
        
        return self.interaction_data.to_numpy()
    

class DB:
    def __init__(self, path):
        self.db = pd.read_csv(path)
    
    def query(self, return_column, cond_column, cond_value):
        result = self.db[self.db[cond_column] == cond_value][return_column]
        if result.shape[0] == 0:
            print(f"No rows for: {cond_column} == {cond_value}")
            return -1
        if result.shape[0] > 1:
            return result.values
        
        return result.values[0]
    
    
class UserDB(DB):
    INDEX = "index"
    ID = "user_profile_id"
    URL = "user_profile_profile_url"
    NAME = "user_profile_name"
    
    def __init__(self, user_data_path="./data/user_db.csv"):
        super().__init__(user_data_path)
    
    def url_by_index(self, idx):
        return self.query(self.URL, self.INDEX, idx)
    
    def name_by_index(self, idx):
        return self.query(self.NAME, self.INDEX, idx)
    
    def id_by_url(self, url):
        return self.query(self.ID, self.URL, url)
    
    def index_by_url(self, url):
        return self.query(self.INDEX, self.URL, url)


class ItemDB(DB):
    INDEX = "index"
    ID = "itemid"
    IMG_URL = "img_url"
    
    def __init__(self, item_data_path="./data/item_db.csv"):
        super().__init__(item_data_path)
        
    def id_by_index(self, idx):
        return self.query(self.ID, self.INDEX, idx)
    
    def img_url_by_index(self, idx):
        return self.query(self.IMG_URL, self.INDEX, idx)


user_db = UserDB()
item_db = ItemDB()
transaction_data = TransactionData().get_transaction_data()
interaction_data = TransactionData().get_interaction_data()
