import argparse
import os
import json
from dataset import Dataset, FMDataset
from model import FMModel
from inference import Inference
import warnings
warnings.filterwarnings("ignore")


def main(args):

    INFERENCE_USER_URL = args.user_url
    K = args.k

    dataset = Dataset(data_dir=args.data_dir)
    transaction_data = dataset.transaction_data

    # check if user_url is valid
    try:
        INFERENCE_USERID = dataset.user_info[INFERENCE_USER_URL]
        print(f"Start inferencing for '{INFERENCE_USER_URL}'...")
    except:
        print("There is no certain USER_URL")
        print("Try again")
        return None

    # dataset
    if args.model == "FM":
        datasetFM = FMDataset(transaction_data)
        ratings_coo = datasetFM.to_coo()

    # model
    if args.model == "FM":
        modelFM = FMModel(model_dir=args.model_dir, ratings_coo=ratings_coo, k=K)
        idxFM = modelFM.predict(INFERENCE_USERID=INFERENCE_USERID)

    file_exists = os.path.exists(os.path.join(args.output_dir, f"output_{INFERENCE_USER_URL}.json"))

    if not file_exists:
        try:
            INFERENCE_USERID = dataset.userid_dict[INFERENCE_USERID]
            inference = Inference(inference_num=K)
            result = inference.proceed_inference(idx=idxFM, itemid_json=dataset.itemid_json, itemid_imageurl_dict=dataset.itemid_imageurl_dict, transaction_data=dataset.transaction_data)
            output = {'user_id': INFERENCE_USER_URL, 'recommendation': result}

            with open(os.path.join(args.output_dir, f"output_{INFERENCE_USER_URL}.json"), "w") as outfile:
                json.dump(output, outfile)
            print(f"Recommended items for {INFERENCE_USER_URL} saved as output_{INFERENCE_USER_URL}.json")
            print("Inference for", INFERENCE_USER_URL, "terminated")

            return output

        except:
            print(f"Not enough transaction data to infer for '{INFERENCE_USER_URL}'...")
            return None
    else:
        print(f"Recommended items for {INFERENCE_USER_URL} already saved as output_{INFERENCE_USER_URL}.json")
        return None
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--user_url", type=str, default="", help="user_url for inference")
    parser.add_argument("--data_dir", type=str, default="./data", help="input data directory")
    parser.add_argument("--model_dir", type=str, default="./model", help="model directory")
    parser.add_argument("--model", type=str, default="FM", help="model type (default: FM)")
    parser.add_argument("--k", type=int, default=10, help="number of recommendations (default: 10)")
    parser.add_argument("--output_dir", type=str, default="output")
    
    args = parser.parse_args()
    os.makedirs(os.path.join(os.getcwd(), args.output_dir), exist_ok=True)
    main(args)