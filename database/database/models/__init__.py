from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .alert import Alert
from .recipient import Recipient
from .subscription import Subscription
