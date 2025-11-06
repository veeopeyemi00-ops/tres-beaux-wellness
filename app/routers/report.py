
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/report/{image_id}", response_class=HTMLResponse)
def report(image_id: str):
    return f"<h1>Tres Beaux — Report</h1><p>Image ID: {image_id}</p><p>Non-diagnostic wellness analysis.</p>"
