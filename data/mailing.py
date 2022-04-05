import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from data.modelbase import SqlAlchemyBase


class Mailing(SqlAlchemyBase):
    __tablename__ = 'mailings'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    start_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    message: str = sa.Column(sa.Text, nullable=False)
    filters: dict = sa.Column(sa.JSON, nullable=False)
    end_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    children = relationship("Message")

    def __repr__(self):
        return f'<MailingList {self.id}>'
