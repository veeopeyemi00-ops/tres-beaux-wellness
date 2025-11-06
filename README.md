
# Tres Beaux Backend (FastAPI) — Admin + Storage Adapter

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```
- JSONL admin log at `storage/datastore.jsonl`
- Switch to S3 by setting `STORAGE_BACKEND=s3` and providing AWS env vars in `.env`

## Endpoints
- POST /upload
- POST /analyze (form-data: image_id)
- GET  /report/{image_id}
- GET  /admin/records
- GET  /admin/record/{image_id}
- DELETE /admin/record/{image_id}
