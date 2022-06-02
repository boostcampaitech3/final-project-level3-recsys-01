import argparse
import multiprocessing
import os
import json
import time
import random

import numpy as np
from tqdm import tqdm
import torch
from torch.utils.data import DataLoader
import torch.optim as optim

from dataset import TrainVAEDataset, ValidVAEDataset
from model import RecVAE
from metric import recall_at_k_batch


def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    random.seed(seed)
    
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default="./data",
                    help='interaction dataset location')
    parser.add_argument('--lr', type=float, default=5e-4,
                        help='initial learning rate')
    parser.add_argument('--gamma', type=float, default=0.005)
    parser.add_argument('--batch_size', type=int, default=20,
                        help='batch size')
    parser.add_argument('--epochs', type=int, default=100,
                        help='upper epoch limit')
    parser.add_argument('--n-enc_epochs', type=int, default=3)
    parser.add_argument('--n-dec_epochs', type=int, default=1)
    parser.add_argument('--latent_dim', type=int, default=200)
    parser.add_argument('--hidden_dim', type=int, default=600)
    
    parser.add_argument('--seed', type=int, default=1111,
                        help='random seed')
    parser.add_argument('--cuda', action='store_true',
                        help='use CUDA')
    
    parser.add_argument('--save_dir', type=str, default='./output',
                        help='path to save the final model')
    parser.add_argument('--exp_descript', type=str, default='./test')
    
    return parser.parse_args()

def train(model, enc_optimizer, dec_optimizer, dataloader, args):
    total_loss = 0.0
    model.train()
    
    for x, y in dataloader:
        x, y = x.to(args.device), y.to(args.device)
        
        for i in range(args.n_enc_epochs):
            enc_optimizer.zero_grad()
            loss, _ = model(x, gamma=args.gamma, dropout_rate=0.5)
            loss.backward()
            enc_optimizer.step()
            
        model.update_prior()
            
            #decoder
        for i in range(args.n_dec_epochs):
            dec_optimizer.zero_grad()
            loss, _ = model(x, gamma=args.gamma, dropout_rate=0.0)
            loss.backward()
            dec_optimizer.step()
        
        total_loss += loss.item()
        
    return total_loss / len(dataloader.dataset)
        
        
    
def validation(model, dataloader, args):
    total_loss = 0.0
    r10 = 0.0
    model.eval()
    
    for x, y in dataloader:
        x, y = x.to(args.device), y.to(args.device)
        loss, pred = model(x)
        
        # Exclude examples from training set
        pred = pred.detach().cpu().numpy()
        pred[x.detach().cpu().numpy().nonzero()] = -np.inf

        r10 += recall_at_k_batch(pred, y.detach().cpu().numpy(), 10).mean()
        total_loss += loss.item()
    
    return total_loss / len(dataloader.dataset), r10 / len(dataloader)

def save_exp_config(args):
    configs = {
        "data": {
            "data path": args.data,
        },
        "model": {
            "epochs": args.epochs,
            "latent_dim": args.latent_dim,
            "hidden_dim": args.hidden_dim,
            
            "learning_rate": args.lr,
            "gamma": args.gamma,
            "batch_size": args.batch_size,
        },
        "etc": {
            "seed": args.seed
        }
    }
    
    with open(os.path.join(args.save_dir, "config.json"), "w") as outfile:
        json.dump(configs, outfile, indent=4)
        
def save_figs(train_loss, valid_loss, r10, args):
    import matplotlib.pyplot as plt
    plt.subplots()
    plt.plot(np.arange(1, args.epochs + 1), train_loss, label="train")
    plt.plot(np.arange(1, args.epochs + 1), valid_loss, label="valid")
    plt.savefig(os.path.join(args.save_dir, "loss.jpg"))
    
    plt.cla()
    
    plt.plot(np.arange(1, args.epochs + 1), r10)
    plt.savefig(os.path.join(args.save_dir, "recall@10.jpg"))

def main(args):
    # dataset, dataloader
    train_dataset = TrainVAEDataset(os.path.join(args.data, "RecVAE_train.csv"))
    valid_dataset = ValidVAEDataset(os.path.join(args.data, "RecVAE_valid.csv"))
    train_dataloader = DataLoader(train_dataset,
                                  batch_size=args.batch_size,
                                  shuffle=True,
                                  num_workers=multiprocessing.cpu_count() // 2)
    valid_dataloader = DataLoader(valid_dataset,
                                  batch_size=len(valid_dataset),
                                  shuffle=False,
                                  num_workers=multiprocessing.cpu_count() // 2)
    
    
    # model & optimizer
    model = RecVAE(args.latent_dim, args.hidden_dim, train_dataset.get_num_items()).to(args.device)
    
    enc_optimizer = optim.Adam(model.encoder.parameters(), lr=args.lr)
    dec_optimizer = optim.Adam(model.decoder.parameters(), lr=args.lr)
    
    train_loss_list = []
    valid_loss_list = []
    valid_r10_list = []
    best_r10 = 0.0
    
    for epoch in range(1, args.epochs + 1):
        epoch_start_time = time.time()
        train_loss = train(model, enc_optimizer, dec_optimizer, train_dataloader, args)
        valid_loss, r10 = validation(model, valid_dataloader, args)
        epoch_end_time = time.time()
        
        train_loss_list.append(train_loss)
        valid_loss_list.append(valid_loss)
        valid_r10_list.append(r10)
        
        if r10 > best_r10:
            best_r10 = r10
            torch.save(model, os.path.join(args.save_dir, "best_model.pt"))
            
        print(f"| end of epoch {epoch} | time: {epoch_end_time - epoch_start_time:4.2f}s "
              f"| train loss: {train_loss:4.2f} "
              f"| valid loss {valid_loss:4.2f} "
              f"| r10 {r10:6.4f} ")
    
    save_figs(train_loss_list, valid_loss_list, valid_r10_list, args)
    


if __name__ == '__main__':
    args = parse_args()
    set_seed(args.seed)
    args.cuda = True if torch.cuda.is_available() else False
    args.device = torch.device("cuda" if args.cuda else "cpu")
    
    args.save_dir = os.path.join(args.save_dir, args.exp_descript)
    os.makedirs(args.save_dir, exist_ok=True)
    
    save_exp_config(args)
    main(args)
