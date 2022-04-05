import asyncio
import json
import datetime

import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from models.mailing.mailing_viewmodel import MailingViewModel
from models.mailing.mailings_viewmodel import MailingsViewModel
from services import mailing_service, send_service, message_service

router = fastapi.APIRouter()


@router.get('/')
@template()
async def index(request: Request):
    vm = MailingsViewModel(request)
    await vm.load()

    result = vm.to_dict()
    for i in range(len(result['mailings'])):
        statistics = await message_service.get_statistics(result['mailings'][i].id)
        if statistics['total']:
            value = round(statistics['true'] * 100 / statistics['total'])
            if value == 100:
                style = 'success'
            elif value >= 50:
                style = 'warning'
            else:
                style = 'danger'
            result['mailings'][i] = {
                'mailing': result['mailings'][i],
                'ready': True,
                'wait': False,
                'completion': value,
                'style': style
            }
        else:
            result['mailings'][i] = {
                'mailing': result['mailings'][i],
                'ready': False,
                'wait': True,
                'completion': 0,
                'style': 'secondary'
            }

    return result


@router.get('/mailing/new')
@template(template_file='mailing/item.pt')
async def new_mailing(request: Request):
    vm = MailingViewModel(request)

    return vm.to_dict()


@router.post('/mailing/new')
@template(template_file='mailing/item.pt')
async def create_mailing(request: Request):
    vm = MailingViewModel(request)
    await vm.load()

    if vm.error:
        return vm.to_dict()

    vm = await mailing_service.create_mailing(vm.to_dict())

    if (vm.start_date <= datetime.datetime.now()) and (vm.end_date >= datetime.datetime.now()):
        await send_service.search_clients(vm)

    response = fastapi.responses.RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

    return response


@router.get('/mailing/remove/{mailing_id}')
@template()
async def remove_mailing(request: Request, mailing_id: int):

    result = await mailing_service.remove_mailing(mailing_id)

    result = status.HTTP_302_FOUND if result else status.HTTP_404_NOT_FOUND

    response = fastapi.responses.RedirectResponse(url='/', status_code=result)

    return response


@router.get('/mailing/edit/{mailing_id}')
@template(template_file='mailing/item.pt')
async def edit_mailing(request: Request, mailing_id: int):
    vm = MailingViewModel(request)
    await vm.receive(mailing_id)

    return vm.to_dict()


@router.post('/mailing/edit/{mailing_id}')
@template(template_file='mailing/item.pt')
async def update_mailing(request: Request):
    vm = MailingViewModel(request)
    await vm.load()

    if vm.error:
        return vm.to_dict()

    vm = await mailing_service.update_mailing(vm.to_dict())

    if (vm.start_date <= datetime.datetime.now()) and (vm.end_date >= datetime.datetime.now()):
        await send_service.search_clients(vm)

    response = fastapi.responses.RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

    return response
