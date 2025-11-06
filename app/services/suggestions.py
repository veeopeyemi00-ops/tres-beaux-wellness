import os, json
from typing import Dict, Any

STORAGE_DIR = os.getenv("STORAGE_DIR", "./storage")
PATH = os.path.join(STORAGE_DIR, "wellness_suggestions.json")


DEFAULTS: Dict[str, Any] = {
    "dryness": "Steam hydration + lightweight scalp oiling 1-2x/week. Focus on mid-shaft to ends; keep scalp light.",
    "buildup": "Do a clarifying cleanse first, then follow with deep hydration in the same session.",
    "redness": "Choose low-tension styles and soothing, fragrance-free care until redness calms.",
    "scaling": "Gentle exfoliating scalp rinse 1x/week, follow with hydration.",
    "oiliness": "Balance with a gentle cleanse; avoid heavy butters and waxes at the scalp.",
    "follicular_clogging": "Clarify periodically; avoid waxy products at the roots.",
    "reduced_density": "Avoid tight-tension styles; add gentle scalp massage 3-5 min/day to support circulation."
}

def _ensure_dir():
    os.makedirs(STORAGE_DIR, exist_ok=True)

def load_suggestions() -> Dict[str, Any]:
    _ensure_dir()
    if not os.path.exists(PATH):
        save_suggestions(DEFAULTS)
        return DEFAULTS.copy()
    try:
        with open(PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        save_suggestions(DEFAULTS)
        return DEFAULTS.copy()
    merged = DEFAULTS.copy()
    merged.update(data or {})
    return merged

def save_suggestions(data: Dict[str, Any]) -> None:
    _ensure_dir()
    clean = { k: data.get(k, DEFAULTS[k]) for k in DEFAULTS.keys() }
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, indent=2)
