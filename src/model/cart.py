from sqlalchemy import text
from sqlalchemy.orm import relationship

from model.base import Base, db


class Cart(Base, db.Model):
    __tablename__ = "cart"
    cart_bookings = relationship("CartBookings", backref="cart")
    cart_order = relationship("Order", backref="cart")
    cart_backups = relationship("OrderBackUp", backref="cart")
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))

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
