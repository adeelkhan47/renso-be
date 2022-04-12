from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from model.base import Base, db


class LocationItemTypes(Base, db.Model):
    __tablename__ = "location_item_type"

    location_id = Column(Integer, ForeignKey("location.id", ondelete="CASCADE"), nullable=False)
    item_type_id = Column(Integer, ForeignKey("item_type.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, location_id, item_type_id):
        self.location_id = location_id
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
    def delete_by_location_id(cls, location_id):
        cls.query.filter(cls.season_id == location_id).delete()
        db.session.commit()
