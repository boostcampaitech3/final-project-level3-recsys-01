import time

from database import transaction_data, item_db


def get_marketplace_url(contract_address):
    return f"https://niftygateway.com/marketplace/collectible/{contract_address}"


def top_k_recommendations(k, idx_list):
    recommendations = {}
    
    for idx in idx_list[:k]:
        item_df = transaction_data[transaction_data.img_url == item_db.img_url_by_index(idx)].drop_duplicates("img_url")
        
        img_url = item_df['nifty_obj_img_url'].values[0]
        extension = item_df['extension'].values[0]
        likes = item_df['nifty_obj_likes'].values[0]
        marketplace_url = get_marketplace_url(item_df["nifty_obj_contract_address"].values[0])
        
        recommendations[img_url] = {'extension': extension, "likes": likes, "url": marketplace_url}
        
    return recommendations
