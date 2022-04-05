import datetime
from typing import Optional, List

from sqlalchemy import and_
from sqlalchemy.future import select

from data import db_session
import httpx

from data.mailing import Mailing
from services import client_service, message_service, mailing_service
from infrastructure.config import JWT, URL

HEADERS = {'Authorization': f'Bearer {JWT}', 'Content-Type': 'application/json; charset=utf-8'}


async def search_clients(mailing: Mailing):
    clients = await client_service.get_clients(mailing.filters)
    for c in clients:
        if not check_timezone(mailing.start_date, mailing.end_date, c.timezone):
            continue
        message = await message_service.check_message(mailing_id=mailing.id, client_id=c.id)
        if message:
            if message.status:
                continue
        else:
            message = await message_service.create_message(mailing_id=mailing.id, client_id=c.id)
        result = await send(message_id=message.id, phone=c.phone, message=mailing.message)
        await message_service.update_status(message_id=message.id, status=result)


async def message_client(mailing_id: int, client_id: int) -> bool:
    message = await message_service.check_message(mailing_id=mailing_id, client_id=client_id)
    if not message or message.status:
        return False
    mailing = await mailing_service.get_mailing_by_id(mailing_id)
    if not mailing:
        return False
    client = await client_service.get_client_by_id(client_id)
    if not client:
        return False
    result = await send(message_id=message.id, phone=client.phone, message=mailing.message)
    await message_service.update_status(message_id=message.id, status=result)
    return True


async def send(message_id: int, phone: str, message: str) -> bool:
    async with httpx.AsyncClient() as client:
        data = {
            'id': message_id,
            'phone': phone,
            'text': message
        }
        response = await client.post(f'{URL}{data["id"]}', json=data, headers=HEADERS)

        return True if response.status_code == 200 else False


def check_timezone(start_date: datetime.datetime, end_date: datetime.datetime, timezone: int) -> bool:
    delta = datetime.datetime.now() + datetime.timedelta(hours=timezone)
    if timezone >= 0:
        if delta <= end_date:
            return True
    else:
        if delta > start_date:
            return True
    return False


async def get_mailings() -> Optional[List[Mailing]]:
    async with db_session.create_async_session() as session:
        query = select(Mailing) \
                .where(and_(Mailing.start_date >= datetime.datetime.now(), Mailing.end_date <= datetime.datetime.now()))

        results = await session.execute(query)
        mailings = results.scalars()

        result: List = []
        for m in mailings:
            status = await message_service.get_statistics(m.id)
            if status['true'] and not status['false']:
                continue
            result.append(m)

        return result


async def send_background():
    mailings = await get_mailings()

    for m in mailings:
        await search_clients(m)
