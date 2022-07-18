from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import text as _text
from model.base import Base, db


class EmailText(Base, db.Model):
    __tablename__ = "email_text"
    text = Column(String(1200), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=_text("False"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True,
                     unique=True)

    def __init__(self, text, user_id):
        self.text = text
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

    @classmethod
    def get_by_user_id(cls, user_id,session=None):
        if not session:
            session = db.session
        return session.query(cls).filter(cls.user_id == user_id).first()
