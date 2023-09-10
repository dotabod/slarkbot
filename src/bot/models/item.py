from sqlalchemy import Column, Integer, String

from . import Base


class Item(Base):
    __tablename__ = "items"

    def __init__(self, id, item_name):
        self.id = id
        self.item_name = item_name

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
