from datetime import datetime

from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship

from . import Base


class Alert(Base):
    __tablename__ = 'alert'

    id_alert = Column(Integer, primary_key=True)
    name = Column(Text)
    url = Column(Text)
    last_check = Column(DateTime, default=datetime.now)

    subscriptions = relationship('Subscription', backref='alert', cascade='all, delete')
