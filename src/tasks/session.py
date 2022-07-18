from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from configuration import configs

engine = create_engine(configs.SQLALCHEMY_DATABASE_URI)


def get_session():
    global engine
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
