from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from model.base import Base, db


class Voucher(Base, db.Model):
    __tablename__ = "voucher"
    code = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    price_factor = Column(Integer, nullable=False, default=100)
    status = Column(Boolean, default=True)

    def __init__(self, code, description, price_factor, status):
        self.code = code
        self.description = description
        self.price_factor = price_factor
        self.status = status

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

    @classmethod
    def get_voucher_by_code(cls, code):
        return cls.query.filter(cls.code == code, cls.status == True).first()
