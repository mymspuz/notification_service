import asyncio

import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from models.message.messages_viewmodel import MessagesViewModel
from services import message_service

router = fastapi.APIRouter()


@router.get('/messages')
@template()
async def index(request: Request):
    vm = MessagesViewModel(request)
    await vm.load()

    return vm.to_dict()
