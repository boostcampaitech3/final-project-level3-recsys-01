import numpy as np
import pandas as pd
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import MetaData, Table, select

from config import *


__all__ = ['db', 'interaction_data']


def getconn():
    conn = Connector().connect(
        MYSQL_CONNECTION_NAME,
        "pymysql",
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB_NAME
    )
    return conn


class DB:
    engine = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=getconn,
        )
    metadata = MetaData()
    
    def __init__(self):
        self.user_table = Table("users", self.metadata, autoload_with=self.engine)
        self.item_table = Table("items", self.metadata, autoload_with=self.engine)
        self.top10_items = Table("top10_items", self.metadata, autoload_with=self.engine)
    
    def _select_from_users(self, cond_column, cond_value):
        with self.engine.connect() as conn:
            stmt = select(self.user_table).where(self.user_table.c[cond_column] == cond_value)
            return conn.execute(stmt)
    
    def _select_from_items(self, cond_column, cond_value):
        with self.engine.connect() as conn:
            stmt = select(self.item_table).where(self.item_table.c[cond_column] == cond_value)
            return conn.execute(stmt)
    
    def find_user_by_id(self, user_id, columns):
        result = self._select_from_users("user_profile_profile_url", user_id).first()
        if result is None:
            return -1
        if len(columns) == 1:
            return result[columns[0]]
        return [result[col] for col in columns]
    
    def find_item_by_index(self, item_id, columns):
        result = self._select_from_items("item_index", item_id).first()
        if len(columns) == 1:
            return result[columns[0]]
        return [result[col] for col in columns]
    
    def find_top10_item_index(self):
        with self.engine.connect() as conn:
            result = conn.execute(select(self.top10_items)).all()
            return [row["item_index"] for row in result]
    
    def get_interaction_data(self):
        with self.engine.connect() as conn:
            df = pd.read_sql_table("interactions", conn)
            df["inter"] = 1
            
            interaction = pd.pivot_table(df,
                                         index=["user_id"],
                                         columns=["item_id"],
                                         values=["inter"],
                                         fill_value=0)
            interaction.columns = np.arange(df.item_id.nunique())
            return interaction.reset_index(drop=True).to_numpy()


db = DB()
interaction_data = db.get_interaction_data()


if __name__ == '__main__':
    name, num_editions, num_likes = db.find_item_by_index(0, ["name", "num_editions", "num_likes"])
    print(name, num_editions, num_likes)
    print(db.find_user_by_id("hugom", ["user_id"]))
    print(interaction_data.shape)
    print(db.find_top10_item_index())
