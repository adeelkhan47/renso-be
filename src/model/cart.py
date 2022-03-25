from sqlalchemy.orm import relationship

from model.base import Base, db


class Cart(Base, db.Model):
    __tablename__ = "cart"
    cart_bookings = relationship("CartBookings", backref="cart")
    cart_order = relationship("Order", backref="cart")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def update(cls, id, data):
        db.session.query(cls).filter(cls.id == id).update(data)
        db.session.commit()
