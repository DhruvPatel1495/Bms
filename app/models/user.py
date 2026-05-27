from sqlalchemy import Column, Integer, String, Float, Boolean

from app.database.db import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    account_id = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    balance = Column(Float, default=0.0)

    is_admin = Column(Boolean, default=False)