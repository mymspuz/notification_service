import datetime
from typing import Optional, List

from starlette.requests import Request

from models.shared.viewmodelbase import ViewModelBase
from services import report_service


class ReportViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.menu[3]['active'] = 'active'

        self.id = request.path_params['mailing_id']
        self.mailing: List[dict] = []

    async def load(self):
        self.mailing = await report_service.get_mailing(self.id)
