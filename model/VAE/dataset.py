import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


class TrainVAEDataset(Dataset):
    def __init__(self, path):
        self.interaction_mat = pd.read_csv(path).to_numpy()
        self.X = torch.FloatTensor(self.interaction_mat)
    
    def __len__(self):
        return self.get_num_users()
    
    def __getitem__(self, idx):
        return self.X[idx], self.X[idx]
    
    def get_num_users(self):
        return self.X.size()[0]
    
    def get_num_items(self):
        return self.X.size()[1]


class ValidVAEDataset(TrainVAEDataset):
    def __init__(self, path, test_size=0.2):
        super().__init__(path)
        self.test_size = test_size
        
        self.X, self.Y = self._validation_split()
    
    def _validation_split(self):
        X, Y = [], []
        for row in self.interaction_mat:
            idxs = np.where(row == 1)[0]
            
            te = np.zeros_like(row, dtype='f')
            te[np.random.choice(idxs, int(self.test_size * len(idxs)), replace=False)] = 1.0
            tr = np.logical_and(np.logical_not(te), row).astype("float")
            
            X.append(tr)
            Y.append(te)
        
        return torch.FloatTensor(np.array(X)), torch.FloatTensor(np.array(Y))
    
    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]


if __name__ == '__main__':
    train_dataset = TrainVAEDataset('data/RecVAE_train.csv')
    valid_dataset = ValidVAEDataset('data/RecVAE_valid.csv')
    print(train_dataset.X.size(), valid_dataset.X.size())
