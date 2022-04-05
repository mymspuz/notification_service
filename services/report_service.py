from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select

from data import db_session
from data.message import Message


async def all_mailings(limit: int = 5) -> List[dict]:
    async with db_session.create_async_session() as session:
        query = select(Message.mailing_id, Message.status, func.count(Message.status)) \
            .group_by(Message.mailing_id, Message.status) \
            .order_by(Message.created_date) \
            .limit(limit)

        mailings = await session.execute(query)
        mailings = mailings.all()

        result: List = []
        temp: dict = {'id': 0, 'ready': 0, 'error': 0, 'sum': 0}
        for i in mailings:
            if temp['id'] != i[0]:
                if temp['id']:
                    result.append(temp)
                temp = {'id': i[0], 'ready': 0, 'error': 0, 'sum': 0}
            if i[1]:
                temp['ready'] = i[2]
            else:
                temp['error'] = i[2]
            temp['sum'] += i[2]
        result.append(temp)

        return result


async def get_mailing(mailing_id: int) -> List[dict]:
    async with db_session.create_async_session() as session:
        query = select(Message).filter(Message.mailing_id == mailing_id)

        mailing = await session.execute(query)
        mailing = mailing.scalars()

        return list({m for m in mailing})
