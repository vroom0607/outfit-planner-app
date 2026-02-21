from pathlib import Path
from uuid import uuid4

from fastapi import Depends, FastAPI, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import weather
import calendar_service
import outfit_engine
import ai_explainer

from database import engine, get_db
from models import Base, Clothing
from wardrobe import router as wardrobe_router

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(wardrobe_router)

Base.metadata.create_all(bind=engine)

# Homepage
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# Upload wardrobe route placeholder
@app.post("/upload")
async def upload_item(
    name: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    extension = Path(image.filename or "").suffix or ".jpg"
    filename = f"{uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / filename

    file_bytes = await image.read()
    file_path.write_bytes(file_bytes)

    clothing = Clothing(
        name=name,
        category=category,
        color="unknown",
        image_path=f"/static/uploads/{filename}",
        tags="",
        times_worn=0,
    )
    db.add(clothing)
    db.commit()
    db.refresh(clothing)

    return RedirectResponse(url="/wardrobe", status_code=303)


@app.get("/wardrobe")
def wardrobe_page(request: Request, db: Session = Depends(get_db)):
    wardrobe = db.query(Clothing).order_by(Clothing.id.desc()).all()
    return templates.TemplateResponse(
        "wardrobe.html",
        {
            "request": request,
            "wardrobe": wardrobe,
        },
    )


# Generate outfit route placeholder
@app.get("/generate")
def generate_outfit(request: Request, db: Session = Depends(get_db)):
    weather_data = weather.get_weather()
    next_event = calendar_service.get_next_event()
    style = outfit_engine.map_event_to_style(next_event)

    wardrobe = db.query(Clothing).all()
    outfit = outfit_engine.generate_outfit(wardrobe, weather_data, style)
    explanation = ai_explainer.generate_explanation(outfit, weather_data, next_event)

    return templates.TemplateResponse(
        "outfit.html",
        {
            "request": request,
            "outfit": outfit,
            "explanation": explanation,
        },
    )
