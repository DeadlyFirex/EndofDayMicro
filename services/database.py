from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from services.config import Config

from bcrypt import hashpw, gensalt

config = Config().get_config()
engine = create_engine(config.database.type + config.database.absolute_path, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import user
    user = user.User(name="Example Administrator", username="admin", email="admin@administrator.com", admin=True,
                     password=hashpw(b'admin', gensalt()).decode("UTF-8"))
    Base.metadata.create_all(bind=engine)
    db_session.add(user)
    db_session.commit()
