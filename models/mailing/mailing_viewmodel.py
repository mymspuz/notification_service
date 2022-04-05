import datetime
from typing import Optional

from starlette.requests import Request

from models.shared.viewmodelbase import ViewModelBase
from services import mailing_service


class MailingViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.menu[0]['active'] = 'active'

        self.id: Optional[int] = None
        self.start_date: Optional[datetime.datetime] = None
        self.end_date: Optional[datetime.datetime] = None
        self.start_date_html: Optional[str] = None
        self.end_date_html: Optional[str] = None
        self.message: Optional[str] = None
        self.filters: dict = {'code': '', 'tag': ''}
        self.statistics: dict = {'true': 0, 'false': 0}

    async def load(self):
        form = await self.request.form()
        self.id = form.get('id')
        self.start_date = datetime.datetime.strptime(form.get('date-start'), '%Y-%m-%dT%H:%M')
        self.end_date = datetime.datetime.strptime(form.get('date-end'), '%Y-%m-%dT%H:%M')
        self.start_date_html = form.get('date-start')
        self.end_date_html = form.get('date-end')
        self.message = form.get('message')
        self.filters['code'] = form.get('code')
        self.filters['tag'] = form.get('tag')

        if not self.start_date or not self.end_date:
            self.error = "Date start and end is required."
        elif not self.message or not self.message.strip():
            self.error = "Message is required."
        elif not self.filters['code'] and (not self.filters['tag'] or not self.filters['tag'].strip()):
            self.error = "Enter code or tag."
        elif self.start_date >= self.end_date:
            self.error = "End Date should be more Start Date."

    async def receive(self, mailing_id: int):
        result = await mailing_service.get_mailing_by_id(mailing_id)
        self.id = result.id
        self.start_date = result.start_date
        self.end_date = result.end_date
        self.start_date_html = self.start_date.strftime('%Y-%m-%dT%H:%M')
        self.end_date_html = self.end_date.strftime('%Y-%m-%dT%H:%M')
        self.message = result.message
        self.filters = result.filters
