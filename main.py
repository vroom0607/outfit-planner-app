from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import weather
import calendar_service
import outfit_engine
import ai_explainer

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Homepage
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Upload wardrobe route placeholder
@app.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# Generate outfit route placeholder
@app.get("/generate")
def generate_outfit(request: Request):
    # Call weather, calendar, outfit_engine, ai_explainer here

    
    return templates.TemplateResponse("outfit.html", {"request": request})