from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import Clothing

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/wardrobe")
def wardrobe_page(request: Request, db: Session = Depends(get_db)):
    wardrobe_items = db.query(Clothing).order_by(Clothing.id.desc()).all()
    return templates.TemplateResponse(
        "wardrobe.html",
        {
            "request": request,
            "wardrobe": wardrobe_items,
        },
    )

@router.post("/wardrobe/delete/{item_id}")
def delete_wardrobe_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Clothing).filter(Clothing.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Wardrobe item not found")

    db.delete(item)
    db.commit()
    return RedirectResponse(url="/wardrobe", status_code=303)
