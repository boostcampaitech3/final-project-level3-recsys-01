# NFT를 골라조

## ‘골라조’를 소개합니다.

## 👨‍👩‍👧Members


|[김동현](https://github.com/donghyyun)|[심재정](https://github.com/Jaejeong98)|[이수연](https://github.com/coding-groot)|[임지원](https://github.com/sophi1127)|[진상우](https://github.com/Jin-s-work)|
| :-------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------: |
| ![그림1](https://user-images.githubusercontent.com/61958748/172278471-584ffaf5-ea6d-4e63-ae77-7cac4dbae899.png)|![그림5](https://user-images.githubusercontent.com/61958748/172278489-00773bd6-080f-41ec-b828-24f4dabc5f98.png)| <img width="140" alt="그림3" src="https://user-images.githubusercontent.com/61958748/172278478-f3bbd8ce-3616-4c37-8fa6-4247e20b469e.png">|  ![그림2](https://user-images.githubusercontent.com/61958748/172278474-f2d54e27-898b-4142-af78-b0e370e43ffc.png)| ![그림4](https://user-images.githubusercontent.com/61958748/172278482-a591c2e4-f4b7-4edf-a390-9e875c2c4226.png)|

## ✨Contribution

-[`김동현`](https://github.com/donghyyun) &nbsp; RecVAE model • Backend

-[`심재정`](https://github.com/Jaejeong98) &nbsp; Frontend

-[`이수연`](https://github.com/coding-groot) &nbsp; Web crawling • GCP connection

-[`임지원`](https://github.com/sophi1127) &nbsp; Data preprocessing • lightFM model

-[`진상우`](https://github.com/Jin-s-work) &nbsp; Frontend • Backend


# 선택지를 반으로 줄이고 싶은 당신을 위해, Nft For Thanos

## 1️⃣ Project Abstract

예술품의 홍수 속에 NFT  예술품 구매에 어려움을 겪는 유저에게 Chrome Extension을 활용해서 도움을 주는 추천시스템

- Why NFT?

    - 예술품 거래, 실물 자산에서 디지털 자산으로!
    
- Why Nifty Gateway?

    - 작품을 등록하기 위한 까다로운 심사 절차 ⇒ 유명 아티스트 작품들 유치!
    
- Why Chrome Extension?

    - Nifty Gateway 홈페이지에서 구매와 추천을 한번에!

## 2️⃣ Demo Video

## 3️⃣ Service Architecture

![Service Architecture](https://user-images.githubusercontent.com/81813324/172277720-8e358429-b3f2-4cba-8148-09f577649201.png)

1. user가 Chrome Extension을 통하여 user ID 입력
2. user ID를 입력받은 Fast API 내 서버는 model의 input으로 user ID를 투입함
3. user ID를 input으로 받은 model은 output으로 추천 아이템 리스트를 받아옴
4. MySQL에 추천할 아이템 리스트 전달
5. MySQL은 아이템들에 대한 메타데이터를 서버로 전달
6. 추천 아이템들의 메타정보가 Chrome Extension을 통해 유저에게 보여짐
- Front End
    - Vanila Javascript로 Chrome Extension 구현
- Back End
    - Fast API & MySQL
    - 서버는 Google Cloud Platform 활용

## 4️⃣ Work Flow

![work flow](https://user-images.githubusercontent.com/81813324/172277819-e18f33c8-53b6-46d1-8472-7f4eaa03e9a6.png
)

### 1. 데이터 수집

- Nifty Gateway API 활용하여 거래 데이터 크롤링
- 2020.9.1~2022.3.31에 진행된 거래에 대해 user정보와 item 정보를 데이터 프레임으로 만듦
    - user: seller ID, purchaser ID
    - item: NFT name, user who made NFT

### 2. 데이터 전처리

- string 타입의 feature들에 대해서 공백을 제거하고, image url이 잘못된 데이터를 제거하는 등 작업
- .Unique한 user와 item을 뽑아냄
    - user: 크롤링한 데이터에서 고유한 식별번호가 존재
    - item: 식별번호가 따로 존재하지 않아,  image url 기준으로 직접 고유 id를 생성
- data sparsity를 줄이기 위해 최소 30건 이상의 거래가 이루어진 user들과 해당 user들이 구매한 모든 item들을 활용
- 모델 학습을 위해 현재 수집된 raw data를 interaction matrix로 변환

### 3. 모델 학습

- 사용한 모델: RecVAE

  - 기존 multi-VAE 모델의 구조를 변형하여 성능을 향상시킨 모델
  - 최종 recall@10: 0.1422

### 4. 모델 배포

하나의 item에 여러 개의 에디션을 보유하는 경우가 존재

⇒ 모든 에디션을 한눈에 비교할 수 있는 marketplace url 제공

## 5️⃣ Future Works

- 이미지 유사성 활용한 content-based filtering model 추가 ⇒ 더 다양한 아이템 추천
- 클릭 기반 아이템 추천 추가⇒더 많은 사용자들에게 서비스 제공 가능
- Load Balancing을 통해 분산처리 구축 ⇒ 대규모 트래픽 대응 가능
