from pydantic import BaseModel


class VowelCountRequest(BaseModel):
    words: list[str]


class VowelCountResponse(BaseModel):
    response: dict
