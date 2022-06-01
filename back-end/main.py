from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

origins = [
    "http://localhost",
    "http://localhost:30001",
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:30001',
]
CORS_ALLOW_ALL_ORIGINS = True



app = FastAPI()
host = "0.0.0.0"
port = 30001

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*']
# )
    


sample_nft = ['https://media.niftygateway.com/image/upload/v1629990317/ADaniel/Jose%20Delbo/BurnDrop/Captain_Apemo_szmxar.jpg',
       'https://media.niftygateway.com/image/upload/v1642000404/Max/OscarLlorens/Oscar_LLorens_Soul_oygs0o.jpg',
       'https://res.cloudinary.com/nifty-gateway/image/upload/v1630084233/AMatthew/JohnVanHamersveldSep1/Clapton/Clapton---02_honv7j.jpg',
       'https://media.niftygateway.com/image/upload/v1614644506/Ashley/FewoCollaboration/1_Victor_and_Victoria_-_FEWOCiOUS_uke8kb.jpg',
       'https://media.niftygateway.com/image/upload/v1640798477/A/MadPups/Curated_9_-_Last_Suspect_xrvi6a.jpg',
       'https://media.niftygateway.com/image/upload/v1645227254/Griffin/Decade2DoodlesConversationsWithTheSun/falling_xizaw0.jpg',
       'https://media.niftygateway.com/image/upload/v1645487601/Griffin/Decade2DoodlesConversationsWithTheSun/Shine_mjzoa2.jpg',
       'http://media.niftygateway.com/image/upload/v1635284003/Max/RefikxARTECHOUSE/Machine_Hallucinations_-_NYC_-0281_qbcdsd.jpg',
       'https://media.niftygateway.com/image/upload/v1647441828/AA/XCOPY/OpenEdition/MAX_PAIN_1_bhtyc0.gif',
       'https://media.niftygateway.com/image/upload/v1629397940/Abigail/x0r/Consensus/FinalAssets/gas_-_Michael_Blau_nrfarj.gif']

@app.get("/")
def get_root_html():
    return FileResponse('../front-end/index.html')

@app.get("/{user_id}") # 추천하는 NFT 링크
def get_user(user_id: str, request: Request):
    return {"user_id": user_id,
            "ip address": request.client.host,
            "recommendation": sample_nft
            }




if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)


