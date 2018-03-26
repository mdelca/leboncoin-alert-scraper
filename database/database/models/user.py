from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'user'

    id_user = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text)
    phone = Column(Text)

    subscriptions = relationship('Subscription', backref='user')
