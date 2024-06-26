from typing import (
    Any,
    Dict,
)

from fastapi import (
    HTTPException,
    status,
)


class DefaultApiException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class InternalServerErrorException(DefaultApiException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Any = {"error": "Some error ocurred!"},
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class ApiInvalidResponseException(DefaultApiException):
    def __init__(
        self,
        status_code: int = 403,
        detail: Any = {"error": "Invalid values for the api"},
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class CurrencyInvalidValuesException(DefaultApiException):
    def __init__(
        self,
        status_code: int = 403,
        detail: Any = {"error": "Invalid values for the api"},
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class MongoRepositoryTransactionsException(DefaultApiException):
    def __init__(
        self,
        status_code: int = 500,
        detail: Any = {"error": "Invalid transaction in mongoDB"},
        headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
