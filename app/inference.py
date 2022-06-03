from database import transaction_data, item_db, user_db
from model import fm_model, recvae_model


def get_inference_results(user_url, K, model_name="RecVAE"):
    user_index = user_db.index_by_url(user_url)
    if user_index < 0: # error case
        return "Invalid user-url"
    
    if model_name == "FM":
        model = fm_model
    if model_name == "RecVAE":
        model = recvae_model
    
    pred_idxs = model.predict(user_index)
    recommendation = top_k_recommendations(K, pred_idxs)
    return {"userid": user_url, "recommendation": recommendation}


def get_marketplace_url(contract_address):
    return f"https://niftygateway.com/marketplace/collectible/{contract_address}"


def top_k_recommendations(k, idx_list):
    recommendations = {}
    
    for idx in idx_list[:k]:
        item_df = transaction_data[transaction_data.img_url == item_db.img_url_by_index(idx)].drop_duplicates("img_url")
        
        img_url = item_df['nifty_obj_img_url'].values[0]
        extension = item_df['extension'].values[0]
        likes = item_df['nifty_obj_likes'].values[0].item()
        marketplace_url = get_marketplace_url(item_df["nifty_obj_contract_address"].values[0])
        
        recommendations[img_url] = {'extension': extension, "likes": likes, "url": marketplace_url}
        
    return recommendations
