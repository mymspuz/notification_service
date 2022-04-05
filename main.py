import fastapi
import fastapi_chameleon
import uvicorn
from pathlib import Path
from starlette.staticfiles import StaticFiles

from data import db_session
from views import mailing, client, message, report


def server_run():
    server_configure()
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)


def server_configure():
    configure_templates()
    configure_routes()
    configure_db()


def configure_db():
    file = (Path(__file__).parent / 'db' / 'notification.sqlite').absolute()
    db_session.global_init(file.as_posix())


def configure_templates():
    fastapi_chameleon.global_init('templates', auto_reload=True)


def configure_routes():
    app.mount('/static', StaticFiles(directory='static'), name='static')
    app.include_router(mailing.router)
    app.include_router(client.router)
    app.include_router(message.router)
    app.include_router(report.router)


app = fastapi.FastAPI()

if __name__ == '__main__':
    server_run()
else:
    server_configure()
