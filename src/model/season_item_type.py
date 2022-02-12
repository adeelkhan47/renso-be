from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from model.base import Base, db


class SeasonItemTypes(Base, db.Model):
    __tablename__ = "season_type"

    season_id = Column(Integer, ForeignKey("season.id", ondelete="CASCADE"), nullable=False)
    item_type_id = Column(Integer, ForeignKey("item_type.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, season_id, item_type_id):
        self.season_id = season_id
        self.item_type_id = item_type_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def delete_by_item_type_id(cls, item_type_id):
        cls.query.filter(cls.item_type_id == item_type_id).delete()
        db.session.commit()

    @classmethod
    def delete_by_season_id(cls, season_id):
        cls.query.filter(cls.season_id == season_id).delete()
        db.session.commit()
