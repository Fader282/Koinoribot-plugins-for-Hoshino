from typing import Optional
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    http_proxy: Optional[str] = 'http://127.0.0.1:7890'
