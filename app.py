from fastapi import FastAPI

from routers.routers import router
from core.settings import settings
from database.init_db import init_db

app = FastAPI(
	title='Blog Agent',
	description='',
	version='0.1.0',
	docs_url='/docs' if settings.DEV else None,
	redoc_url='/redoc' if settings.DEV else None,
	license_info={
		'name': 'GNU Affero General Public License v3.0 or later',
		'identifier': 'AGPL-3.0-or-later',
		'url': 'https://spdx.org/licenses/AGPL-3.0-or-later.html',
	},
)

app.include_router(router)
@app.on_event("startup")
async def startup():
    await init_db()