from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from model.base import Base, db


class Location(Base, db.Model):
    __tablename__ = "location"
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price_factor = Column(Integer, nullable=False, default=100)
    item_locations = relationship("ItemLocation", backref="location")
    itemTypeLocations = relationship("LocationItemTypes", backref="location")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)
    booking_location = relationship("Booking", backref="location")
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))

    def __init__(self, name, description, price_factor, user_id):
        self.name = name
        self.description = description
        self.price_factor = price_factor
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()


    @classmethod
    def soft_delete(cls, id):
        db.session.query(cls).filter(cls.id == id).update({"is_deleted": True})
        db.session.commit()

    @classmethod
    def update(cls, id, data):
        db.session.query(cls).filter(cls.id == id).update(data)
        db.session.commit()
