import importlib
import pkgutil
from pathlib import Path
from fastapi import APIRouter


def load_routers() -> list[APIRouter]:
    routers = []
    package_dir = Path(__file__).parent
    package_name = __name__

    for _, mod, _ in pkgutil.iter_modules([str(package_dir)]):
        module = importlib.import_module(f'{package_name}.{mod}')
        if hasattr(module, 'router'):
            routers.append(module.router)
    return routers
