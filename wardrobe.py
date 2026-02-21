from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import Clothing

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/wardrobe")
def view_wardrobe(request: Request, db: Session = Depends(get_db)):
    items = db.query(Clothing).all()
    return templates.TemplateResponse("wardrobe.html", {"request": request, "wardrobe": items})


@router.delete("/wardrobe/{item_id}")
def delete_wardrobe_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Clothing).filter(Clothing.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Wardrobe item not found")

    db.delete(item)
    db.commit()
    return JSONResponse({"message": "Wardrobe item deleted successfully"})
