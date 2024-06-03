import logging
from typing import Annotated

from fastapi import (
    APIRouter,
    Path,
    Query,
    status,
)
from fastapi.responses import JSONResponse

from app.api.v1.currency_converter.exceptions import GenericApiException
from app.api.v1.currency_converter.models import (
    Currency,
    UpdateCurrency,
)
from app.api.v1.currency_converter.service import CurrencyConverterService
from app.exceptions.default_exceptions import DefaultApiException

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Currency"])


@router.get(
    path="/currency/{acronym}",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
def get_currency(
    acronym: Annotated[str, Path(title="Currency Acronym to return")]
) -> JSONResponse:
    """
    Returns the currency we created in our database by they name
    """
    service = CurrencyConverterService()
    try:
        if response := service.get_currency(acronym):
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as error:
        logger.error("Unmapped error", extra={"error": error})
        raise GenericApiException()


@router.post(
    path="/currency/{acronym}",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
def create_currency(
    acronym: Annotated[str, Path(title="Currency Acronym to create")],
    payload: Currency,
) -> JSONResponse:
    """
    Create a currency in our database
    """
    payload.acronym = acronym
    service = CurrencyConverterService()
    try:
        id = service.create_currency(payload)
    except DefaultApiException as error:
        raise error
    except Exception as error:
        logger.error("Unmapped error", extra={"error": error})
        raise GenericApiException()
    return JSONResponse(content={"id": id}, status_code=status.HTTP_201_CREATED)


@router.put(
    path="/currency/{acronym}",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
def update_currency(
    acronym: Annotated[str, Path(title="Currency Acronym to update")],
    payload: UpdateCurrency,
) -> JSONResponse:

    service = CurrencyConverterService()
    payload.acronym = acronym
    try:
        if service.update_currency(payload):
            return JSONResponse(
                content={"acronym": acronym}, status_code=status.HTTP_200_OK
            )
    except DefaultApiException as error:
        raise error
    except Exception as error:
        logger.error("Unmapped error", extra={"error": error})
        raise GenericApiException()


@router.delete(
    path="/currency/{acronym}",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
def delete_currency_by_acronym(
    acronym: Annotated[str, Path(title="Currency Acronym to delete")],
) -> JSONResponse:

    service = CurrencyConverterService()
    try:
        acronym = service.delete_currency(acronym)
    except DefaultApiException as error:
        raise error
    except Exception as error:
        logger.error("Unmapped error", extra={"error": error})
        raise GenericApiException()
    return JSONResponse(content={"acronym": acronym}, status_code=status.HTTP_200_OK)


@router.get(
    path="/currencies",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
def get_all_currency() -> JSONResponse:
    """
    Returns all the currencys we created in our database
    """
    service = CurrencyConverterService()
    try:
        if response := service.get_all_currency():
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except Exception as error:
        logger.error("Unmapped error", extra={"error": error})
        raise GenericApiException()


@router.get(
    path="/currency_exchange",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
def currency_exchange(
    from_: str = Query(alias="from"),
    to: str = Query(),
    amount: float = Query(),
) -> JSONResponse:
    """
    Return the value of the amount of a conversion between one currency and another
    """
    # Always leaving the values ​​in upper case.
    from_, to = from_.upper(), to.upper()
    service = CurrencyConverterService()
    try:
        converted_value = service.currency_exchange(from_, to, amount)
        return JSONResponse(
            content={"converted_value": converted_value}, status_code=status.HTTP_200_OK
        )
    except DefaultApiException as error:
        raise error
    except Exception as error:
        logger.error("Unmapped error", extra={"error": error})
        raise GenericApiException()
