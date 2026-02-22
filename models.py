from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Clothing(Base):
    __tablename__ = "clothes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)   
    color = Column(String)
    image_path = Column(String)
    tags = Column(String)      
    times_worn = Column(Integer, default=0)