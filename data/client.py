import sqlalchemy as sa

from data.modelbase import SqlAlchemyBase


class Client(SqlAlchemyBase):
    __tablename__ = 'clients'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    phone: str = sa.Column(sa.String(length=11), unique=True, nullable=False)
    phone_code: str = sa.Column(sa.String(length=3), index=True, nullable=False)
    tag: str = sa.Column(sa.String(length=20), index=True)
    timezone: int = sa.Column(sa.SmallInteger, nullable=False)

    def __repr__(self):
        return f'Client {self.id}'
