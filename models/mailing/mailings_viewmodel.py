from typing import List

from starlette.requests import Request

from data.mailing import Mailing
from services import mailing_service
from models.shared.viewmodelbase import ViewModelBase


class MailingsViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.menu[0]['active'] = 'active'

        self.mailings: List[Mailing] = []

    async def load(self):
        self.mailings = await mailing_service.latest_mailing(limit=7)
