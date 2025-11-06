
from fastapi import APIRouter, HTTPException, Body
from app.services.store import list_records, get_record, delete_record
from app.services.suggestions import load_suggestions, save_suggestions


router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/records")
def records(limit: int = 200):
    return {"items": list_records(limit)}

@router.get("/record/{image_id}")
def record(image_id: str):
    rec = get_record(image_id)
    if not rec:
        raise HTTPException(404, "not found")
    return rec

@router.delete("/record/{image_id}")
def remove(image_id: str):
    ok = delete_record(image_id)
    return {"deleted": bool(ok)}
# NEW — editable Wellness Library
@router.get("/wellness-suggestions")
def get_wellness_suggestions():
    return load_suggestions()

@router.post("/wellness-suggestions")
def set_wellness_suggestions(payload: dict = Body(...)):
    save_suggestions(payload)
    return {"ok": True}
