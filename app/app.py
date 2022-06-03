import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from inference import get_inference_results


app = FastAPI()
host = "0.0.0.0"
port = 30001

origins = [
    f"http://{host}",
    "http://{host}:{port}",
]

CORS_ALLOWED_ORIGINS = [
    'http://{host}:{port}',
]
CORS_ALLOW_ALL_ORIGINS = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{user_id}") # 추천하는 NFT 링크
def get_user(user_id: str):
    result = get_inference_results(user_id, 10)
    if isinstance(result, dict):
        return result


if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)


