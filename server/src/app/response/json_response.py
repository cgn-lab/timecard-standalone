from typing import Any
import orjson
from fastapi.responses import JSONResponse as BaseJSONResponse


class JSONResponse(BaseJSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_NON_STR_KEYS)
