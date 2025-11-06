
import os, json, time
from typing import Dict, List, Optional

LOG_PATH = os.path.join(os.getenv("STORAGE_DIR", "./storage"), "datastore.jsonl")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def _write(rec: Dict):
    rec["ts"] = rec.get("ts") or time.time()
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")

def record_upload(image_id: str):
    _write({"type": "upload", "image_id": image_id})

def record_analysis(image_id: str, quality: Dict, findings: Dict, model_version: str):
    _write({
        "type": "analysis",
        "image_id": image_id,
        "quality": quality,
        "findings": findings,
        "model_version": model_version
    })

def list_records(limit: int = 200) -> List[Dict]:
    if not os.path.exists(LOG_PATH):
        return []
    lines = open(LOG_PATH, "r", encoding="utf-8").read().splitlines()
    folded: Dict[str, Dict] = {}
    for line in lines:
        try:
            rec = json.loads(line)
        except Exception:
            continue
        iid = rec.get("image_id", "unknown")
        prev = folded.get(iid, {"image_id": iid})
        prev.update(rec)
        folded[iid] = prev
    items = sorted(folded.values(), key=lambda r: r.get("ts", 0), reverse=True)
    return items[:limit]

def get_record(image_id: str):
    return next((r for r in list_records(10000) if r.get("image_id")==image_id), None)

def delete_record(image_id: str) -> bool:
    if not os.path.exists(LOG_PATH):
        return False
    kept = []
    removed = False
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("image_id")==image_id:
                removed = True
                continue
            kept.append(line)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for line in kept:
            f.write(line)
    return removed
