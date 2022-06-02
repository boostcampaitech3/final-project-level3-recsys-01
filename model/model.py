import numpy as np
import os
import joblib
from lightfm.evaluation import recall_at_k
import warnings
warnings.filterwarnings("ignore")


class FMModel:

    def __init__(self, model_dir: str, ratings_coo, k):
        self.ratings_coo = ratings_coo
        self.k = k
        self.trained_model = joblib.load(os.path.join(model_dir, "FM/FMmodel/FM_best_model.pkl")) 
        ratings_recall = recall_at_k(self.trained_model, self.ratings_coo, k = self.k).mean()
        print(f"Loaded FM best model where recall@{self.k} is {ratings_recall}")


    def predict(self, INFERENCE_USERID):

        ratings_array = self.ratings_coo.toarray()

        predict_item_ids = np.where(ratings_array[INFERENCE_USERID] == 0)[0]
        predict_userids = np.full((len(predict_item_ids)), INFERENCE_USERID)
        prediction = self.trained_model.predict(predict_userids, predict_item_ids)

        idx = sorted(range(len(prediction)), reverse=True, key=lambda k: prediction[k])
        idx = [predict_item_ids[x] for x in idx]

        return idx