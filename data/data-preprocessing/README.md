# final-project-level3-recsys-01

## 필요한 파일
    - requirements.txt
    - raw_data.csv
    - data-preprocessing.ipynb
    - splitted_data.ipynb: 실제로 학습에 사용할 데이터와 train/test 데이터 저장하는 코드
    - run.sh

## 돌려야 하는 코드
```
run.sh
```

## 생성된 파일
    - data-preprocessing.py: data-preprocessing.ipynb 파일을 py 파일로 변환
    - userid.json: raw_data의 userid를 0부터 맵핑
    - itemid.json: raw_data의 itemid를 0부터 맵핑
    - preprocessed_data.csv: raw_data.csv를 가공한 파일 (nifty_obj_img_url이 http로 시작하는 거래내역만 남김)
    - interaction.py: interaction.ipynb 파일을 py 파일로 변환
    - active_min30.csv: userid, itemid 기준으로 unique한 item만 남긴 data
    - test_min30.csv: active_min30 중 userid 별 timestamp 기준 마지막 5개 데이터
    - train_min30.csv: active_min30 중 test_min30 데이터를 제외한 데이터
    - test_answer_min30.csv: test_min30를 userid와 itemid column만 남긴 정답
    - train_interaction_min30_sparse9916.csv: train_min30 중 userid와 itemid의 interaction 데이터
    - interaction_itemid_imageurl_min30.json: itemid와 nifty_obj_img_url을 맵핑
    - interaction_userid_min30.json: interaction 데이터로 사용할 userid만 남긴 뒤 0부터 맵핑
    - interaction_itemid_min30.json: interaction 데이터로 사용할 itemid만 남긴 뒤 0부터 맵핑
