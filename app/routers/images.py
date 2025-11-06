
import os
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from PIL import Image
from app.services.analyzer import analyze_image
from app.services.store import record_upload, record_analysis
from app.services.storage import save_bytes, local_path_for

router = APIRouter()
STORAGE_DIR = os.getenv("STORAGE_DIR", "./storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
  ext = os.path.splitext(file.filename)[1].lower() or ".jpg"
  image_id = str(uuid4())
  data = await file.read()
  # save via storage adapter (local or S3)
  path_or_uri = save_bytes(image_id, ext, data)
  # Verify if local
  local_path = local_path_for(image_id)
  if local_path:
      try:
          Image.open(local_path).verify()
      except Exception as e:
          if os.path.exists(local_path):
              os.remove(local_path)
          raise HTTPException(status_code=400, detail=f"Invalid image: {e}")
  record_upload(image_id)
  return {"image_id": image_id}

@router.post("/analyze")
async def analyze(image_id: str = Form(...)):
  local_path = local_path_for(image_id)
  if not local_path:
      raise HTTPException(status_code=404, detail="Image not found")
  quality, findings, suggestions, version = analyze_image(local_path)
  record_analysis(image_id, quality, findings, version)
  return {
      "image_id": image_id,
      "quality": quality,
      "findings": findings,
      "suggestions": suggestions,
      "model_version": version
  }
