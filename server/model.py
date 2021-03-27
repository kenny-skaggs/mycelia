from sqlalchemy import Boolean, Column, DateTime, Integer, Text, VARCHAR
from sqlalchemy.ext.declarative import declarative_base


base_model = declarative_base()


class Account(base_model):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    privilege = Column(Text, nullable=False)
    last_login = Column(Text, nullable=False)
    date_created = Column(DateTime, nullable=False)
    grade_level = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False)
    alt_pass = Column('pass', Text, nullable=False)
    password = Column(Text)
    username = Column(Text)
    clever_id = Column(VARCHAR(255), server_default=None, index=True)
    ignore_updates = Column(Boolean, nullable=False)
    student_number = Column(Text)
    setup_token = Column(Text)
    is_self_registered = Column(Boolean, nullable=False)
