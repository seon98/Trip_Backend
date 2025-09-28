from fastapi import FastAPI

app = FastAPI(title="떠나봄 Backend API", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "떠나봄 여행 플랫폼 백엔드 서버 준비 완료"}