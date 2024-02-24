from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

print("tables")

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    email = Column(String(200), unique=True)
    username = Column(String(200), unique=True)
    password_hash = Column(String(200))
    operation = relationship('Operation', back_populates='user')

class Operation(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'), index=True)
    date = Column(String(200))
    kind = Column(String(200))
    amount = Column(Numeric(10, 2))
    description = Column(String(200), nullable=True)
    user = relationship('User', back_populates='operation')
