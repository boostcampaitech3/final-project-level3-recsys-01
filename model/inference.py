import time
# https://github.com/spyoungtech/grequests
import grequests
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import warnings
warnings.filterwarnings("ignore")

class Inference:
    
    def __init__(self, inference_num) -> None:

        self.inference_num = inference_num

    def api_url_list(self, x, y):
        url_list = []
        for i in range(len(x)):
            url_list.append(f"https://api.niftygateway.com/nifty/metadata-minted/?contractAddress={x[i]}&tokenId={y[i]}")
        return url_list

    def marketplace_url_list(self, x, y):
        url_list = []
        for i in range(len(x)):
            url_list.append(f"https://niftygateway.com/marketplace/item/{x[i]}/{y[i]}")
        return url_list

    def proceed_inference(self, idx, itemid_json, itemid_imageurl_dict, transaction_data):

        tok = time.time()

        INFERENCE_NUM = self.inference_num

        result = {}
        itemid_dict = itemid_json.set_index('index').to_dict()['itemid']
        idx_num = 0

        while len(result) < INFERENCE_NUM:
            recommended_item = itemid_dict[idx[idx_num]]
            recommended_image = itemid_imageurl_dict[recommended_item]
            recommended_df = transaction_data[transaction_data.img_url == recommended_image]
            recommended_image_url = list(recommended_df['nifty_obj_img_url'])[0]
            cand_df = recommended_df[['nifty_obj_contract_address', 'nifty_obj_token_id', 'nifty_obj_name', 'nifty_obj_likes', 'nifty_obj_total_num_editions', 'extension']].drop_duplicates().reset_index(drop=True)
            cand_nifty_obj_contract_address = list(cand_df.nifty_obj_contract_address)
            cand_nifty_obj_token_id = list(cand_df.nifty_obj_token_id)
            api_url_list = self.api_url_list(cand_nifty_obj_contract_address, cand_nifty_obj_token_id)
            marketplace_url_list = self.marketplace_url_list(cand_nifty_obj_contract_address, cand_nifty_obj_token_id)
            cand_nifty_obj_name = list(cand_df.nifty_obj_name)
            likes = list(cand_df.nifty_obj_likes)[0]
            cand_nifty_obj_total_num_editions = list(cand_df.nifty_obj_total_num_editions)
            extension = list(cand_df.extension)[0]
            
            on_sale = []
            sellOrder = []
            listings = []

            NUM_SESSIONS = 10
            sessions = [requests.Session() for _ in range(NUM_SESSIONS)]
            retries = Retry(total=5,
                            backoff_factor=0.1,
                            status_forcelist=[500, 502, 503, 504])
            for s in sessions:
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))

            reqs = []
            i = 0
            for url in api_url_list:
                reqs.append(grequests.get(url, session=sessions[i % NUM_SESSIONS]))
                i += 1
            responses = grequests.imap(reqs, size=NUM_SESSIONS)

            for response in responses:
                api_request = response.json()['niftyMetadata']
                on_sale.append(api_request['currently_on_sale'])
                sellOrder.append(api_request['sellOrder'])
                listings.append(api_request['listings'])

            cand_df['url']=api_url_list
            cand_df['marketplace_url_list']=marketplace_url_list
            cand_df['on_sale'] = on_sale
            cand_df['sellOrder'] = sellOrder
            cand_df['listings'] = listings
            cand_df['names'] = cand_nifty_obj_name
            cand_df['editions'] = cand_nifty_obj_total_num_editions
            new_cand_df = cand_df[cand_df['on_sale']==True]
            new_cand_df['price']=['$'+str(float(list(new_cand_df.sellOrder)[i]['priceInCents'])/100) if 'priceInCents' in list(new_cand_df.sellOrder)[i] else str(list(new_cand_df.listings)[i][0]['baseListingPrice']['amount'])+list(new_cand_df.listings)[i][0]['baseListingPrice']['currency'] for i in range(new_cand_df.shape[0])]

            if new_cand_df.shape[0] > 0:
                result[recommended_image_url] = {'extension': extension, 'likes':likes, 'url': list(new_cand_df.marketplace_url_list), 'name': list(new_cand_df.names), 'editions': list(new_cand_df.editions), 'price': list(new_cand_df.price)}
                print(f"{len(result)}th recommendation completed")
            idx_num += 1
        
        tick = time.time()
        print(f"Runtime of the inference is {tick - tok}")
        return result