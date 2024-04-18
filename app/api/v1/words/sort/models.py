from pydantic import BaseModel


class SortWordsRequest(BaseModel):
    words: list[str]
    order: str


class SortWordsResponse(BaseModel):
    response: list
