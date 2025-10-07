from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routers import accommodations, flights, users, auth, pages, bookings, admin, admin_pages

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pages.router)
app.include_router(accommodations.router)
app.include_router(flights.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(admin.router)
app.include_router(admin_pages.router)

@app.get("/api-root")
def read_api_root():
    return {"message": "API 서버 루트"}