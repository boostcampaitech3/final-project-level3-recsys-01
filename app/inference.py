from database import db
from model import recvae_model


def get_inference_results(user_url, K):
    user_index = db.find_user_by_id(user_url, ["user_index"])
    if user_index < 0: # when invalid user id is given return top10 popular items
        return {"userid": user_url, 
                "recommendation": top_k_recommendations(K, db.find_top10_item_index()), 
                "over30": False}
    
    model = recvae_model
    
    pred_idxs = model.predict(user_index)
    recommendation = top_k_recommendations(K, pred_idxs)
    return {"userid": user_url, 
            "recommendation": recommendation, 
            "over30": True}


def get_marketplace_url(contract_address):
    return f"https://niftygateway.com/marketplace/collectible/{contract_address}"


def top_k_recommendations(k, idx_list):
    recommendations = {}
    search_columns = ["img_url", "extension", "num_likes", "contract_address"]
    
    for idx in idx_list[:k]:
        img_url, extension, likes, contract_address = db.find_item_by_index(idx, search_columns)
        marketplace_url = get_marketplace_url(contract_address)
        
        recommendations[img_url] = {'extension': extension, "likes": likes, "url": marketplace_url}
        
    return recommendations
