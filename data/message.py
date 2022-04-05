import datetime
import sqlalchemy as sa

from data.modelbase import SqlAlchemyBase


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    status: bool = sa.Column(sa.Boolean, default=False, nullable=False)
    mailing_id = sa.Column(sa.Integer, sa.ForeignKey('mailings.id'))
    client_id = sa.Column(sa.Integer, sa.ForeignKey('clients.id'))

    def __repr__(self):
        return f'Message {self.id}'
