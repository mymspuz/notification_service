import datetime
from typing import List, Optional, Dict

from sqlalchemy import func
from sqlalchemy.future import select

from data import db_session
from data.message import Message


async def get_messages(limit: int = 15) -> List[Message]:
    async with db_session.create_async_session() as session:
        query = select(Message) \
            .order_by(Message.mailing_id, Message.client_id) \
            .limit(limit)

        results = await session.execute(query)
        messages = results.scalars()

        return list({m for m in messages})


async def create_message(mailing_id: int, client_id: int) -> Message:
    message = Message()
    message.mailing_id = mailing_id
    message.client_id = client_id

    async with db_session.create_async_session() as session:
        session.add(message)
        await session.commit()

    return message


async def update_status(message_id: int, status: bool) -> Message:
    async with db_session.create_async_session() as session:
        src = await get_message_by_id(message_id)
        src.created_date = datetime.datetime.now()
        src.status = status
        session.add(src)
        await session.commit()
        return src


async def check_message(mailing_id: int, client_id: int) -> Optional[Message]:
    async with db_session.create_async_session() as session:
        query = select(Message).filter(Message.client_id == client_id, Message.mailing_id == mailing_id)
        result = await session.execute(query)

        return result.scalar_one_or_none()


async def get_message_by_id(message_id: int) -> Optional[Message]:
    async with db_session.create_async_session() as session:
        query = select(Message).filter(Message.id == message_id)
        result = await session.execute(query)

        return result.scalar_one_or_none()


async def get_statistics(mailing_id: int) -> Optional[Dict]:
    async with db_session.create_async_session() as session:
        query = select(Message.status, func.count(Message.status)) \
                .where(Message.mailing_id == mailing_id) \
                .group_by(Message.status)

        results = await session.execute(query)
        results = results.all()
        statistics = {'true': 0, 'false': 0, 'total': 0}

        for i in results:
            if i[0]:
                statistics['true'] = i[1]
            else:
                statistics['false'] = i[1]
            statistics['total'] += i[1]

        return statistics
