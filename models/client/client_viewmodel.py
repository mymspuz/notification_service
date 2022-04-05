from typing import Optional, List

from starlette.requests import Request

from models.shared.viewmodelbase import ViewModelBase
from services import client_service


class ClientViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.menu[1]['active'] = 'active'

        self.id: Optional[int] = None
        self.phone: Optional[str] = None
        self.tag: Optional[str] = None
        self.timezone: Optional[int] = None

    async def load(self):
        form = await self.request.form()
        self.id = form.get('id')
        self.phone = form.get('phone')
        self.tag = form.get('tag')
        self.timezone = form.get('timezone')

        if not self.phone or not self.phone.strip():
            self.error = 'Phone is required.'
        elif len(self.phone) != 10 or not self.phone.isalnum():
            self.error = 'Phone incorrect'
        elif not self.timezone or not self.timezone.strip():
            self.error = 'Timezone is required.'
        elif not self.timezone.replace('-', '').isdigit() or not int(self.timezone) in list(range(-12, 13)):
            self.error = 'Timezone is incorrect.'

        # self.phone = f'7{self.phone}'

    async def receive(self, client_id: int):
        result = await client_service.get_client_by_id(client_id)
        self.id = result.id
        self.phone = result.phone[1:]
        self.tag = result.tag
        self.timezone = result.timezone
