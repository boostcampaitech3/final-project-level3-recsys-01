import joblib
import os

import numpy as np
import torch

from database import interaction_data
from ._RecVAE import RecVAE

WEIGHT_DIR= "./model/weight"


class FMModel:
    def __init__(self):
        self.trained_model = joblib.load(os.path.join(WEIGHT_DIR, "FM/FM_best_model.pkl")) 

    def predict(self, INFERENCE_USERID):
        predict_item_ids = np.where(interaction_data[INFERENCE_USERID] == 0)[0]
        predict_userids = np.full((len(predict_item_ids)), INFERENCE_USERID)
        prediction = self.trained_model.predict(predict_userids, predict_item_ids)

        idx = sorted(range(len(prediction)), reverse=True, key=lambda k: prediction[k])
        idx = [predict_item_ids[x] for x in idx]

        return idx


class RecVAEModel:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.trained_model = RecVAE(200, 600, interaction_data.shape[1])
        self.trained_model = torch.load(os.path.join(WEIGHT_DIR, "RecVAE/best_model.pt"))
        self.trained_model.to(self.device).eval()
    
    def predict(self, user_id):
        X = torch.FloatTensor(interaction_data[user_id]).unsqueeze(0)
        _, pred = self.trained_model(X.to(self.device))
        pred = pred.detach().cpu().squeeze().numpy()
        
        pred[X.squeeze().numpy().nonzero()] = -np.inf
        return (-pred).argsort().tolist()


if __name__ == "__main__":
    print(RecVAEModel().predict(0))
