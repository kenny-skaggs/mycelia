import atexit
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder

from datastore import Settings


class Connection:
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super(Connection, cls).__new__(cls)
            instance.session_factory = cls._build_session_factory()
            cls._instance = instance

        return cls._instance

    @contextmanager
    def get_new_session(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        finally:
            session.close()

    @classmethod
    def _build_session_factory(cls) -> sessionmaker:
        db_user = Settings.get('DB_USERNAME')
        db_password = Settings.get('DB_PASSWORD')

        proxy = cls._start_ssh_proxy()
        engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@127.0.0.1:{proxy.local_bind_port}/republiccs')
        return sessionmaker(bind=engine, expire_on_commit=False)

    @classmethod
    def _start_ssh_proxy(cls) -> SSHTunnelForwarder:
        ssh_user = Settings.get('SSH_USERNAME')
        ssh_password = Settings.get('SSH_PASSWORD')

        server = SSHTunnelForwarder(
            ssh_address_or_host=('platform.republiccs.org', 22),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=('platform.republiccs.org', 3306)
        )
        server.start()
        atexit.register(server.stop)

        return server
