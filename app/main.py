
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import images, report, admin

app = FastAPI(title=os.getenv("APP_NAME", "Tres Beaux AI Scalp Wellness Scanner"))
allowed = os.getenv("ALLOWED_ORIGINS", "*")
app.add_middleware(CORSMiddleware, allow_origins=[allowed] if allowed!="*" else ["*"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(images.router)
app.include_router(report.router)
app.include_router(admin.router)
