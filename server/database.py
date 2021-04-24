import atexit
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder

from datastore import Settings

ssh_user = Settings.get('SSH_USERNAME')
ssh_password = Settings.get('SSH_PASSWORD')
db_user = Settings.get('DB_USERNAME')
db_password = Settings.get('DB_PASSWORD')

server = SSHTunnelForwarder(
    ssh_address_or_host=('platform.republiccs.org', 22),
    ssh_username=ssh_user,
    ssh_password=ssh_password,
    remote_bind_address=('platform.republiccs.org', 3306)
)
server.start()
atexit.register(server.stop)

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@127.0.0.1:{server.local_bind_port}/republiccs')
session_factory = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def get_new_session():
    session = session_factory()
    try:
        yield session
        session.commit()
    finally:
        session.close()


with get_new_session() as session:
    print('count', session.execute('select count(*) from user;'))
