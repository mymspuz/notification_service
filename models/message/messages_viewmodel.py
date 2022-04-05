from typing import List

from starlette.requests import Request

from data.message import Message
from services import message_service
from models.shared.viewmodelbase import ViewModelBase


class MessagesViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.menu[2]['active'] = 'active'

        self.messages: List[Message] = []

    async def load(self):
        self.messages = await message_service.get_messages()
