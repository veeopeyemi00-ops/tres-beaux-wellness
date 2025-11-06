
import os, random
MODEL_VERSION = "scalp-v0.0.2-placeholder"
def _sev(p: float) -> str:
    if p < 0.25: return "none"
    if p < 0.5: return "mild"
    if p < 0.75: return "moderate"
    return "severe"
def analyze_image(path: str):
    seed = sum(bytearray(os.path.basename(path), "utf-8"))
    rnd = random.Random(seed)
    quality = {"blur": round(rnd.random()*0.3, 2), "glare": round(rnd.random()*0.3, 2), "usable": True}
    findings = {
        "dryness": {"prob": round(rnd.random(),2), "severity": "none"},
        "builup": {"prob": round(rnd.random(),2), "severity": "none"},
        "redness": {"prob": round(rnd.random(),2), "severity": "none"},
        "scaling": {"prob": round(rnd.random(),2), "severity": "none"},
        "oiliness": {"prob": round(rnd.random(),2), "severity": "none"},
        "follicular_clogging": {"prob": round(rnd.random(),2), "severity": "none"},
        "reduced_density": {"prob": round(rnd.random(),2), "severity": "none"}
    }
    if "builup" in findings:  # fix key typo to 'buildup'
        findings["buildup"] = findings.pop("builup")
    for k,v in findings.items(): v["severity"] = _sev(v["prob"])
    suggestions = []
    if findings["buildup"]["prob"] > 0.5 or findings["oiliness"]["prob"] > 0.5: suggestions.append("Clarifying cleanse followed by hydration.")
    if findings["dryness"]["prob"] > 0.5 or findings["scaling"]["prob"] > 0.5: suggestions.append("Steam hydration + lightweight scalp oiling 2–3x/week.")
    if findings["redness"]["prob"] > 0.6: suggestions.append("Reduce mechanical tension; switch to gentle, fragrance-free products.")
    if findings["reduced_density"]["prob"] > 0.5: suggestions.append("Limit tight-tension styles; add gentle scalp massage to support circulation.")
    if not suggestions: suggestions = ["Your scalp appears balanced. Maintain your routine and check back in 2–4 weeks."]
    return quality, findings, suggestions, MODEL_VERSION
