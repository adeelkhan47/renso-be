from sqlalchemy import text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from model.base import Base, db


class Voucher(Base, db.Model):
    __tablename__ = "voucher"
    code = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price_factor = Column(Integer, nullable=False, default=100)
    counter = Column(Integer, nullable=True, default=0)
    status = Column(Boolean, default=True)
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)

    def __init__(self, code, description, price_factor, status, user_id, counter):
        self.code = code
        self.description = description
        self.price_factor = price_factor
        self.status = status
        self.user_id = user_id
        self.counter = counter

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

    @classmethod
    def get_voucher_by_code(cls, code, user_id):
        return cls.query.filter(cls.code == code, cls.status == True, cls.user_id == user_id, cls.is_deleted == False).first()
