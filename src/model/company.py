from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from model.base import Base, db


class Company(Base, db.Model):
    __tablename__ = "company"
    name = Column(String, nullable=True, unique=True)
    street = Column(String, nullable=True)
    street_number = Column(String, nullable=True)
    zipcode = Column(String, nullable=True)
    city = Column(String, nullable=True)
    commercial_registered_number = Column(String, nullable=True)
    legal_representative = Column(String, nullable=True)
    email_for_taxs = Column(String, nullable=True)
    company_tax_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    bate_number = Column(Integer, nullable=True, default=1)

    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))
    sub_category_company = relationship("ItemSubType", backref="company")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)

    def __init__(self, name, street, street_number, zipcode, city, commercial_registered_number, legal_representative,
                 email_for_taxs, company_tax_number, email, bate_number, user_id):
        self.name = name
        self.street = street
        self.street_number = street_number
        self.zipcode = zipcode
        self.city = city
        self.commercial_registered_number = commercial_registered_number
        self.legal_representative = legal_representative
        self.email_for_taxs = email_for_taxs
        self.company_tax_number = company_tax_number
        self.bate_number = bate_number
        self.email = email
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def update(cls, id, data,session=None):
        if not session:
            session = db.session
        session.query(cls).filter(cls.id == id).update(data)
        session.commit()


    @classmethod
    def soft_delete(cls, id):
        db.session.query(cls).filter(cls.id == id).update({"is_deleted": True})
        db.session.commit()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
