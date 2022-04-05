import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from models.client.clients_viewmodel import ClientsViewModel
from models.client.client_viewmodel import ClientViewModel
from services import client_service, send_service

router = fastapi.APIRouter()


@router.get('/clients')
@template()
async def index(request: Request):
    vm = ClientsViewModel(request)
    await vm.load()

    return vm.to_dict()


@router.get('/client/send/')
@template(template_file='client/item.pt')
async def new_client(request: Request, mid: int = 0, cid: int = 0):
    result = await send_service.message_client(mid, cid)

    response = fastapi.responses.RedirectResponse(url=f'/report/{mid}', status_code=status.HTTP_302_FOUND)

    return response


@router.get('/client/new')
@template(template_file='client/item.pt')
async def new_client(request: Request):
    vm = ClientViewModel(request)

    return vm.to_dict()


@router.post('/client/new')
@template(template_file='client/item.pt')
async def create_client(request: Request):
    vm = ClientViewModel(request)
    await vm.load()

    if vm.error:
        return vm.to_dict()

    await client_service.create_client(vm.to_dict())

    response = fastapi.responses.RedirectResponse(url='/clients', status_code=status.HTTP_302_FOUND)

    return response


@router.get('/client/remove/{client_id}')
@template()
async def remove_client(request: Request, client_id: int):

    result = await client_service.remove_client(client_id)

    result = status.HTTP_302_FOUND if result else status.HTTP_409_CONFLICT

    response = fastapi.responses.RedirectResponse(url='/clients', status_code=result)

    return response


@router.get('/client/edit/{client_id}')
@template(template_file='client/item.pt')
async def edit_client(request: Request, client_id: int):
    vm = ClientViewModel(request)
    await vm.receive(client_id)

    return vm.to_dict()


@router.post('/client/edit/{client_id}')
@template(template_file='client/item.pt')
async def update_client(request: Request):
    vm = ClientViewModel(request)
    await vm.load()

    if vm.error:
        return vm.to_dict()

    result = await client_service.update_client(vm.to_dict())

    result = status.HTTP_302_FOUND if result else status.HTTP_409_CONFLICT

    response = fastapi.responses.RedirectResponse(url='/clients', status_code=result)

    return response
