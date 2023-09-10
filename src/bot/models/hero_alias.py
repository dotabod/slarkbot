from sqlalchemy import ARRAY, Column, Integer, String

from . import Base


class HeroAlias(Base):
    __tablename__ = "hero_aliases"

    def __init__(self, id, hero_id, alias):
        self.id = id
        self.hero_id = hero_id
        self.alias = alias

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer)
    alias = Column(String)
