from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.future import select

from data import db_session
from data.client import Client
from data.message import Message


async def latest_client(limit: int = 15) -> List[Client]:
    async with db_session.create_async_session() as session:
        query = select(Client) \
            .order_by(Client.phone) \
            .limit(limit)

        results = await session.execute(query)
        clients = results.scalars()

        result: List = []
        for c in clients:
            status = await check_client(c.id)
            result.append({'client': c, 'status': True if status else False})

        return result


async def create_client(src: dict) -> Client:
    client = Client()
    client.phone = f"7{src['phone']}"
    client.phone_code = src['phone'][:3]
    client.tag = src['tag'].strip() if src['tag'].strip() else None
    client.timezone = int(src['timezone'])

    async with db_session.create_async_session() as session:
        session.add(client)
        await session.commit()

    return client


async def remove_client(client_id: int) -> Optional[Client]:
    async with db_session.create_async_session() as session:
        check = await check_client(client_id)
        if check:
            return None

        client = await session.get(Client, client_id)

        if client:
            await session.delete(client)
            await session.commit()

    return client


async def update_client(new: dict) -> Optional[Client]:
    async with db_session.create_async_session() as session:
        check = await check_client(int(new['id']))
        if check:
            return None
        is_change = False
        src = await get_client_by_id(int(new['id']))
        if src.phone != f"7{new['phone']}":
            is_change = True
            src.phone = f"7{new['phone']}"
            src.phone_code = new['phone'][:3]
        if src.tag != new['tag']:
            is_change = True
            src.tag = new['tag']
        if src.timezone != new['timezone']:
            is_change = True
            src.timezone = new['timezone']
        if is_change:
            session.add(src)
            await session.commit()
        return src


async def get_client_by_id(client_id: int) -> Optional[Client]:
    async with db_session.create_async_session() as session:
        query = select(Client).filter(Client.id == client_id)
        result = await session.execute(query)

        return result.scalar_one_or_none()


async def get_clients(filters: dict) -> List[Client]:
    async with db_session.create_async_session() as session:
        if filters['code'] and filters['tag']:
            query = select(Client) \
                .order_by(Client.phone) \
                .where(and_(Client.phone_code == filters['code'], Client.tag == filters['tag']))
        elif filters['code']:
            query = select(Client) \
                .order_by(Client.phone) \
                .where(Client.phone_code == filters['code'])
        elif filters['tag']:
            query = select(Client) \
                .order_by(Client.phone) \
                .where(Client.tag == filters['tag'])

        result = await session.execute(query)
        clients = result.scalars()

        return list({c for c in clients})


async def check_client(client_id: int) -> Optional[Message]:
    async with db_session.create_async_session() as session:
        query = select(Message).filter(Message.client_id == client_id)

        result = await session.execute(query)

        return result.scalars().first()
