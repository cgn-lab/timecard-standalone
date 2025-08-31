import pkgutil
import importlib
from pathlib import Path


def load_models() -> None:
    """
    同じディレクトリ内の全てのモデルファイルを import して
    SQLAlchemy の Base.metadata に登録されるようにする
    """
    package_dir = Path(__file__).parent
    package_name = __name__

    for _, mod_name, _ in pkgutil.iter_modules([str(package_dir)]):
        importlib.import_module(f"{package_name}.{mod_name}")
