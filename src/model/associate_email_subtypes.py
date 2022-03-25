from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from model.base import Base, db


class AssociateEmailSubtype(Base, db.Model):
    __tablename__ = "associate_email_subtype"

    associate_email_id = Column(Integer, ForeignKey("associate_email.id", ondelete="CASCADE"), nullable=False)
    item_subtype_id = Column(Integer, ForeignKey("item_subtype.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, associate_email_id, item_subtype_id):
        self.associate_email_id = associate_email_id
        self.item_subtype_id = item_subtype_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def delete_by_item_subtype_id(cls, item_subtype_id):
        cls.query.filter(cls.item_subtype_id == item_subtype_id).delete()
        db.session.commit()

    @classmethod
    def delete_by_email_id(cls, a_email_id):
        cls.query.filter(cls.associate_email_id == a_email_id).delete()
        db.session.commit()