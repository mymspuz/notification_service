import asyncio
import datetime

import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from models.report.report_viewmodel import ReportViewModel
from models.report.reports_viewmodel import ReportsViewModel

router = fastapi.APIRouter()


@router.get('/reports')
@template()
async def index(request: Request):
    vm = ReportsViewModel(request)
    await vm.load()

    return vm.to_dict()


@router.get('/report/{mailing_id}')
@template(template_file='report/item.pt')
async def get_report_mailing(request: Request):
    vm = ReportViewModel(request)
    await vm.load()

    return vm.to_dict()
