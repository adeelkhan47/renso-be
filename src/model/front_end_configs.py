from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from model.base import Base, db


class FrontEndCofigs(Base, db.Model):
    __tablename__ = "front_end_configs"
    logo = Column(String, default="")
    front_end_url = Column(String, default="")
    email = Column(String, default="")
    email_password = Column(String, default="")
    link1_name = Column(String, nullable=True)
    link2_name = Column(String, nullable=True)
    link1 = Column(String, nullable=True)
    link2 = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)

    def __init__(self, url, front_end_url, email, email_password, user_id, link1_name, link2_name, link1, link2):
        self.url = url
        self.user_id = user_id
        self.front_end_url = front_end_url
        self.email = email
        self.email_password = email_password
        self.link1 = link1
        self.link2 = link2
        self.link1_name = link1_name
        self.link2_name = link2_name

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
    def get_by_user_id(cls, user_id, session=None):
        if not session:
            session = db.session
        row = session.query(cls).filter(cls.user_id == user_id).first()
        return row
