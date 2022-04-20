from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from model.base import Base, db


class FrontEndCofigs(Base, db.Model):
    __tablename__ = "front_end_configs"
    logo = Column(String, default="")
    front_end_url = Column(String, default="")
    email = Column(String, default="")
    email_password = Column(String, default="")
    privacy_policy_link = Column(String, default="")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    def __init__(self, url, front_end_url, user_id, email, email_password, privacy_policy_link):
        self.url = url
        self.user_id = user_id
        self.front_end_url = front_end_url
        self.email = email
        self.email_password = email_password
        self.privacy_policy_link = privacy_policy_link

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
    def get_by_user_id(cls, user_id):
        row = cls.query.filter(cls.user_id == user_id).first()
        return row
