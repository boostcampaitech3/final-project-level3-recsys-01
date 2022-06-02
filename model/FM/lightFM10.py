# https://making.lyst.com/lightfm/docs/lightfm.html

import numpy as np
import pandas as pd

import joblib
import wandb

import argparse
from sklearn import preprocessing

from tqdm import tqdm

from scipy import sparse

from lightfm import LightFM
from lightfm.evaluation import recall_at_k


def main():

    wandb.login()

    parser = argparse.ArgumentParser()

    parser.add_argument("--model", type=str, default="logistic")
    parser.add_argument("--num_components", type=int, default=10)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--num_epochs", type=int, default=100)
    parser.add_argument("--user_alpha", type=float, default=0.0)
    parser.add_argument("--learning_rate", type=float, default=0.05)
    parser.add_argument("--learning_schedule", type=str, default="adagrad")
    parser.add_argument("--rho", type=float, default=0.95)
    parser.add_argument("--epsilon", type=float, default=1e-06)
    parser.add_argument("--max_sampled", type=int, default=10)
    parser.add_argument("--submission", type=str, default="lightFM")

    args = parser.parse_args()

    print(args.submission)

    wandb.init(project="NFT", config=vars(args), entity="recsys_01")

    # 평점 데이터
    ratings_df = pd.read_csv("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/train10_min30.csv")
    ratings_df["rating"] = 1
    ratings_df = ratings_df[["userid", "itemid", "rating"]]

    df = ratings_df.copy()
    users = df["userid"]
    movies = df["itemid"]

    le_users = preprocessing.LabelEncoder()
    le_users.fit(users)
    user_index = le_users.transform(users)

    le_movies = preprocessing.LabelEncoder()
    le_movies.fit(movies)
    movie_index = le_movies.transform(movies)

    coo_shape = (len(le_users.classes_), len(le_movies.classes_))

    ratings_coo = sparse.coo_matrix((df["rating"], (user_index, movie_index)), shape=coo_shape, dtype = np.int32)
    ratings_coo.shape

    # warp model without item feature

    MODEL = args.model
    NUM_COMPONENTS = args.num_components
    K = args.k
    N = args.n
    NUM_EPOCHS = args.num_epochs
    USER_ALPHA = args.user_alpha
    LEARNING_RATE = args.learning_rate
    LEARNING_SCHEDULE = args.learning_schedule
    RHO = args.rho
    EPSILON = args.epsilon
    MAX_SAMPLED = args.max_sampled

    # Define a new model instance
    model = LightFM(loss=MODEL,
                    random_state=42,
                    user_alpha=USER_ALPHA,
                    no_components=NUM_COMPONENTS,
                    k=K,
                    n=N,
                    learning_rate=LEARNING_RATE,
                    learning_schedule=LEARNING_SCHEDULE,
                    rho=RHO,
                    epsilon=EPSILON,
                    max_sampled=MAX_SAMPLED)

    model_wo_item_feature = model.fit(ratings_coo,
                    epochs=NUM_EPOCHS,
                    verbose = True)

    ratings_recall = recall_at_k(model_wo_item_feature,
                        ratings_coo,
                        k = 10).mean()
    print(args.submission, " ratings set recall@10: ", ratings_recall)

    joblib.dump(model_wo_item_feature, "/opt/ml/final-project-level3-recsys-01/model/FM/FMmodel/" + args.submission + '.pkl')

    user_output = []
    item_output = []
    ratings_array = ratings_coo.toarray()

    for i in tqdm(range(len(le_users.classes_))):
        predict_item_ids = np.where(ratings_array[i] == 0)[0]
        predict_userids = np.full((len(predict_item_ids)), i)
        prediction = model_wo_item_feature.predict(predict_userids, predict_item_ids)
        
        ind = prediction.argpartition(-10)[-10:]
        user_output.extend([i]*10)
        item_output.extend(predict_item_ids[ind])

    submission = pd.DataFrame()
    submission["userid"] = le_users.inverse_transform(user_output)
    submission["itemid"] = le_movies.inverse_transform(item_output)
    submission.to_csv("/opt/ml/final-project-level3-recsys-01/model/FM/FMoutput/" + args.submission + ".csv", index=False)
    print("Done!!!")

    # calculate score
    answer = pd.read_csv("/opt/ml/final-project-level3-recsys-01/data/data-preprocessing/test10_answer_min30.csv")
    score = []
    for x in answer.userid.unique():
        y_true = set(answer[answer['userid']==x]['itemid'])
        y_predict = set(submission[submission['userid']==x]['itemid'])
        score.append(len(y_true.intersection(y_predict))/10)
    print('score: ', sum(score)/len(score))
    wandb.log({"train recall@10": ratings_recall, "score": sum(score)/len(score)})

if __name__ == "__main__":
    wandb.login()
    main()