from typing import List

from starlette.requests import Request

from models.shared.viewmodelbase import ViewModelBase
from services import report_service


class ReportsViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.menu[3]['active'] = 'active'

        self.mailings: List[dict] = []

    async def load(self):
        self.mailings = await report_service.all_mailings()
