from typing import List

from starlette.requests import Request

from data.client import Client
from services import client_service
from models.shared.viewmodelbase import ViewModelBase


class ClientsViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.menu[1]['active'] = 'active'

        self.clients: List[Client] = []

    async def load(self):
        self.clients = await client_service.latest_client()
