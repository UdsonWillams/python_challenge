from typing import (
    Any,
    Dict,
)

from fastapi import status

from app.exceptions.default_exceptions import DefaultApiException


class SortWordsException(DefaultApiException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = {"error": "Some error ocurred!"},
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
