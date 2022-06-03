from database import user_db
from model import fm_model, recvae_model
from inference import top_k_recommendations


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

    
if __name__ == "__main__":
    print(get_inference_results(user_url="vllg", K=10, model_name="RecVAE"))
    print(get_inference_results(user_url="vllg", K=10, model_name="FM"))
