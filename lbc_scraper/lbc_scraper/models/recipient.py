from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from . import Base


class Recipient(Base):
    __tablename__ = 'recipient'

    id_recipient = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text)
    phone = Column(Text)

    subscriptions = relationship('Subscription', backref='recipient')
