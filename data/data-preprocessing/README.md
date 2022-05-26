# final-project-level3-recsys-01

## 필요한 파일
    - requirements.txt
    - raw_data.csv
    - data-preprocessing.ipynb
    - interaction.ipynb
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
    - itemid_imageurl.json: itemid와 nifty_obj_img_url을 맵핑
    - interaction_userid.json: interaction 데이터로 사용할 userid만 남긴 뒤 0부터 맵핑
    - interaction_itemid.json: interaction 데이터로 사용할 itemid만 남긴 뒤 0부터 맵핑
    - interaction.csv: userid x itemid의 interaction 데이터
