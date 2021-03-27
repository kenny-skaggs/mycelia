from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root@localhost/republiccs?charset=latin1')
session_factory = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def get_new_session():
    session = session_factory()
    try:
        yield session
        session.commit()
    finally:
        session.close()
