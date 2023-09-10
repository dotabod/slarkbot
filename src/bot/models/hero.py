from sqlalchemy import ARRAY, Column, Integer, String

from . import Base


class Hero(Base):
    __tablename__ = "heroes"

    def __init__(self, id, name, localized_name, primary_attr, roles, img):
        self.id = id
        self.name = name
        self.localized_name = localized_name
        self.primary_attr = primary_attr
        self.roles = roles
        self.img = img

    id = Column(Integer, primary_key=True)
    name = Column(String)
    localized_name = Column(String)
    primary_attr = Column(String)
    roles = Column(ARRAY(String))
    img = Column(String)
