import os
from logging import getLogger
from fastapi import APIRouter
from app.response import *
from lib import Config
from lib.utils import path_of, read_file

log = getLogger('api')
router = APIRouter()


@router.get('/{path:path}')
async def get(path: str):

    if path == 'index.html':
        return RedirectResponse('/')

    if path == '':
        path = 'index.html'

    file = path_of(Config.PUBLIC_DIR, path)
    if not file.startswith(Config.PUBLIC_DIR):
        return Response(None, 403)
    if not os.path.isfile(file):
        return Response(None, 404)

    if file.endswith('.json'):
        return JSONResponse(read_file(file))
    elif file.endswith(('.htm', '.html')):
        return HTMLResponse(read_file(file))
    else:
        return FileResponse(file)
