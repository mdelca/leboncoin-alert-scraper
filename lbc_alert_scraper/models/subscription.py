from sqlalchemy import Column, Integer, ForeignKey

from . import Base


class Subscription(Base):
    __tablename__ = 'subscription'

    id_subscription = Column(Integer, primary_key=True)
    id_recipient = Column(Integer, ForeignKey('recipient.id_recipient'))
    id_alert = Column(Integer, ForeignKey('alert.id_alert'))
