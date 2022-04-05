from typing import List, Optional

from sqlalchemy.future import select

from data import db_session
from data.mailing import Mailing
from data.message import Message


async def latest_mailing(limit: int = 5) -> List[Mailing]:
    async with db_session.create_async_session() as session:
        query = select(Mailing) \
            .order_by(Mailing.start_date) \
            .limit(limit)

        results = await session.execute(query)
        mailings = results.scalars()

        return list({m for m in mailings})


async def create_mailing(src: dict) -> Mailing:
    mailing = Mailing()
    mailing.start_date = src['start_date']
    mailing.end_date = src['end_date']
    mailing.message = src['message']
    mailing.filters = src['filters']

    async with db_session.create_async_session() as session:
        session.add(mailing)
        await session.commit()

    return mailing


async def remove_mailing(mailing_id: int) -> Optional[Mailing]:
    async with db_session.create_async_session() as session:

        check = await check_mailing(mailing_id)
        if check:
            return None

        mailing = await session.get(Mailing, mailing_id)

        if mailing:
            await session.delete(mailing)
            await session.commit()

    return mailing


async def edit_mailing(src: dict) -> Mailing:
    mailing = Mailing()
    mailing.start_date = src['start_date']
    mailing.end_date = src['end_date']
    mailing.message = src['message']
    mailing.filters = src['filters']

    async with db_session.create_async_session() as session:
        session.add(mailing)
        await session.commit()

    return mailing


async def update_mailing(new: dict) -> Optional[Mailing]:
    async with db_session.create_async_session() as session:

        check = await check_mailing(int(new['id']))
        if check:
            return None

        is_change = False
        src = await get_mailing_by_id(int(new['id']))
        if src.start_date != new['start_date']:
            is_change = True
            src.start_date = new['start_date']
        if src.end_date != new['end_date']:
            is_change = True
            src.end_date = new['end_date']
        if src.message != new['message']:
            is_change = True
            src.message = new['message']
        if src.filters != new['filters']:
            is_change = True
            src.filters = new['filters']
        if is_change:
            session.add(src)
            await session.commit()
        return src


async def get_mailing_by_id(mailing_id: int) -> Optional[Mailing]:
    async with db_session.create_async_session() as session:
        query = select(Mailing).filter(Mailing.id == mailing_id)
        result = await session.execute(query)

        return result.scalar_one_or_none()


async def check_mailing(mailing_id: int) -> Optional[Message]:
    async with db_session.create_async_session() as session:
        query = select(Message).filter(Message.mailing_id == mailing_id)
        result = await session.execute(query)

        return result.scalar_one_or_none()
