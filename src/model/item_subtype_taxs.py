from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from model.base import Base, db


class ItemSubTypeTaxs(Base, db.Model):
    __tablename__ = "item_subtype_taxs"
    item_sub_type_id = Column(Integer, ForeignKey("item_subtype.id", ondelete="CASCADE"), nullable=False)
    tax_id = Column(Integer, ForeignKey("tax.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, item_sub_type_id, tax_id):
        self.item_sub_type_id = item_sub_type_id
        self.tax_id = tax_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def delete_by_tax_id(cls, tax_id):
        cls.query.filter(cls.tax_id == tax_id).delete()
        db.session.commit()

    @classmethod
    def delete_by_item_sub_type_id(cls, item_sub_type_id):
        cls.query.filter(cls.item_sub_type_id == item_sub_type_id).delete()
        db.session.commit()
