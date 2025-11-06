
import os
from pathlib import Path
from typing import Optional

BACKEND = os.getenv("STORAGE_BACKEND", "local")
LOCAL_DIR = os.getenv("STORAGE_DIR", "./storage")

# Optional S3 config
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET = os.getenv("AWS_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

def save_bytes(image_id: str, ext: str, data: bytes) -> str:
    if BACKEND == "s3":
        import boto3
        key = f"uploads/{image_id}{ext}"
        s3 = boto3.client("s3", region_name=AWS_REGION,
                          aws_access_key_id=AWS_ACCESS_KEY_ID or None,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY or None)
        s3.put_object(Bucket=AWS_BUCKET, Key=key, Body=data, ContentType="image/jpeg")
        return f"s3://{AWS_BUCKET}/{key}"
    else:
        Path(LOCAL_DIR).mkdir(parents=True, exist_ok=True)
        path = os.path.join(LOCAL_DIR, f"{image_id}{ext}")
        with open(path, "wb") as f:
            f.write(data)
        return path

def local_path_for(image_id: str) -> Optional[str]:
    if BACKEND == "s3":
        # For analysis you’d normally stream from S3; for simplicity we download to temp
        import boto3, tempfile
        s3 = boto3.client("s3", region_name=AWS_REGION,
                          aws_access_key_id=AWS_ACCESS_KEY_ID or None,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY or None)
        for ext in [".jpg",".jpeg",".png",".bmp",".webp"]:
            key = f"uploads/{image_id}{ext}"
            try:
                tmp = tempfile.mktemp(suffix=ext)
                s3.download_file(AWS_BUCKET, key, tmp)
                return tmp
            except Exception:
                continue
        return None
    else:
        for ext in [".jpg",".jpeg",".png",".bmp",".webp"]:
            p = os.path.join(LOCAL_DIR, f"{image_id}{ext}")
            if os.path.exists(p):
                return p
        return None
