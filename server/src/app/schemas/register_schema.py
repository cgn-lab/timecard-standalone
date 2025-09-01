from pydantic import BaseModel, Field


class PostRegisterRequest(BaseModel):
    username: str = Field(..., alias="UserName", min_length=4)
    password: str = Field(..., alias="Password", min_length=8)


__all__ = [
    'PostRegisterRequest'
]
