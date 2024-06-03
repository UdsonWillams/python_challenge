import json
from unittest.mock import (
    Mock,
    patch,
)

from fastapi import status
from fastapi.responses import JSONResponse
from httpx import Response

from app.api.v1.currency_converter.exceptions import (
    CurrencyServiceException,
    GenericApiException,
    ValidateAcronymException,
)
from app.api.v1.currency_converter.models import Currency
from app.api.v1.currency_converter.views import (
    create_currency,
    currency_exchange,
    delete_currency_by_acronym,
    get_all_currency,
    get_currency,
)
from app.exceptions.default_exceptions import (
    ApiInvalidResponseException,
    MongoRepositoryTransactionsException,
)
from tests.unit import DefaultTestCase

default_date_format = "%d/%m/%Y"


class CurrencyViewsTestCase(DefaultTestCase):

    def setUp(self) -> None:
        return super().setUp()

    @patch("app.repositories.redis_repository.RedisRepository.create")
    @patch("app.repositories.redis_repository.RedisRepository.get")
    @patch("app.repositories.mongo_repository.MongoRepository.get_by_acronym")
    def test_get_currency(
        self, mock_get_by_acronym: Mock, redis_mock_get: Mock, redis_mock_create: Mock
    ):

        redis_mock_get.return_value = False
        redis_mock_create.return_value = False
        return_mock = Currency(
            acronym="TEST", name="TESTE-NAME", dolar_price_reference=10
        )
        mock_get_by_acronym.return_value = return_mock.model_dump()

        response: JSONResponse = currency_exchange(from_="USD", to="BRL", amount=200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.body), {"converted_value": "200.000000"})

    @patch("app.repositories.redis_repository.RedisRepository.get")
    @patch("app.repositories.mongo_repository.MongoRepository.get_by_acronym")
    @patch("app.services.awesomeapi.AwesomeApiService._execute")
    def test_get_currency_passing_in_the_api(
        self, mock_currency_api: Mock, mock_get_by_acronym: Mock, redis_mock: Mock
    ):
        redis_mock.return_value = False
        mock_get_by_acronym.side_effect = MongoRepositoryTransactionsException
        mock_currency_api.return_value = Response(
            status.HTTP_200_OK, content='{"USDBRL": {"bid": 1}}'
        )
        response: JSONResponse = currency_exchange(from_="USD", to="BRL", amount=200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.body), {"converted_value": "200.00"})

    @patch("app.repositories.redis_repository.RedisRepository.get")
    @patch("app.repositories.mongo_repository.MongoRepository.get_by_acronym")
    @patch("app.services.awesomeapi.AwesomeApiService._execute")
    def test_get_currency_passing_in_the_api_and_return_it_invalid_response(
        self, mock_currency_api: Mock, mock_get_by_acronym: Mock, redis_mock: Mock
    ):
        redis_mock.return_value = False
        mock_get_by_acronym.side_effect = MongoRepositoryTransactionsException
        mock_currency_api.return_value = Response(
            status.HTTP_400_BAD_REQUEST, content='{"error": "bad-request"}'
        )
        with self.assertRaises(ApiInvalidResponseException) as context_error:
            currency_exchange(from_="USD", to="BRL", amount=200)
        self.assertEqual(context_error.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            context_error.exception.detail, {"error": "Invalid values for the api"}
        )

    @patch("app.repositories.mongo_repository.MongoRepository.get_by_acronym")
    def test_get_currency_raise_generic_error(self, mock_get_by_acronym: Mock):

        return_value = Currency(
            acronym="TEST", name="TESTE-NAME", dolar_price_reference=10
        ).model_dump()
        mock_get_by_acronym.side_effect = return_value

        with self.assertRaises(GenericApiException) as context_error:
            currency_exchange(from_="USD", to="BRL", amount=200)
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertEqual(
            context_error.exception.detail, {"error": "Some error ocurred!"}
        )

    @patch("app.repositories.mongo_repository.MongoRepository.get_by_acronym")
    def test_get_one_currency(self, mock_get_by_acronym: Mock):

        return_value = Currency(
            acronym="TEST", name="TESTE-NAME", dolar_price_reference=10
        ).model_dump()
        mock_get_by_acronym.return_value = return_value

        response: JSONResponse = get_currency(acronym="USD")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.body), return_value)

    @patch("app.repositories.mongo_repository.MongoRepository.get_by_acronym")
    def test_get_currency_not_found_value(self, mock_get_by_acronym: Mock):

        mock_get_by_acronym.return_value = None
        response: JSONResponse = get_currency(acronym="USD")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.body), {})

    @patch("app.repositories.mongo_repository.MongoRepository.get_by_acronym")
    def test_get_currency_repository_raises_unexpected_error(
        self, mock_get_by_acronym: Mock
    ):

        mock_get_by_acronym.side_effect = Exception("test error")

        with self.assertRaises(GenericApiException) as context_error:
            get_currency(acronym="USD")
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertEqual(
            context_error.exception.detail, {"error": "Some error ocurred!"}
        )

    @patch("app.repositories.redis_repository.RedisRepository.get")
    @patch("app.repositories.mongo_repository.MongoRepository.get_all_currency")
    def test_get_all_currency(self, redis_mock: Mock, mock_get_by_acronym: Mock):

        redis_mock.return_value = False
        return_value = Currency(
            acronym="TEST", name="TESTE-NAME", dolar_price_reference=10
        ).model_dump()
        return_value = [return_value]
        mock_get_by_acronym.return_value = return_value

        response: JSONResponse = get_all_currency()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.body), return_value)

    @patch("app.repositories.mongo_repository.MongoRepository.get_all_currency")
    def test_get_all_currency_and_repository_raises_unexpected_error(
        self, mock_get_by_acronym: Mock
    ):

        mock_get_by_acronym.side_effect = Exception("test error")

        with self.assertRaises(GenericApiException) as context_error:
            get_all_currency()
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertEqual(
            context_error.exception.detail, {"error": "Some error ocurred!"}
        )

    @patch("app.repositories.mongo_repository.MongoRepository.create")
    def test_create_currency(self, mock_repository_create: Mock):

        payload = Currency(acronym="TEST", name="TESTE-NAME", dolar_price_reference=10)
        mock_repository_create.return_value = None

        response: JSONResponse = create_currency(payload.acronym, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.body), {"id": payload.id})

    @patch("app.repositories.mongo_repository.MongoRepository.create")
    def test_create_currency_repository_raises_unexpected_error(
        self, mock_repository_create: Mock
    ):

        mock_repository_create.side_effect = Exception("test error")
        payload = Currency(acronym="TEST", name="TESTE-NAME", dolar_price_reference=10)

        with self.assertRaises(CurrencyServiceException) as context_error:
            create_currency(payload.acronym, payload)
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertEqual(
            context_error.exception.detail, {"error": "Error to create currency"}
        )

    @patch("app.repositories.mongo_repository.MongoRepository.create")
    def test_create_model_raises_validate_error(self, mock_repository_create: Mock):

        mock_repository_create.side_effect = Exception("test error")
        with self.assertRaises(ValidateAcronymException) as context_error:
            create_currency(
                Currency(
                    acronym="TEST-ACRONYNM", name="TESTE-NAME", dolar_price_reference=10
                )
            )
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertEqual(
            context_error.exception.detail, {"error": "Acronym value not valid"}
        )

    @patch(
        "app.api.v1.currency_converter.service.CurrencyConverterService.create_currency"
    )
    def test_create_currency_endpoint_raises_unexpected_error(
        self, mock_repository_create: Mock
    ):

        mock_repository_create.side_effect = Exception("test error")
        payload = Currency(acronym="TEST", name="TESTE-NAME", dolar_price_reference=10)

        with self.assertRaises(GenericApiException) as context_error:
            create_currency(payload.acronym, payload)
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertEqual(
            context_error.exception.detail, {"error": "Some error ocurred!"}
        )

    @patch(
        "app.api.v1.currency_converter.service.CurrencyConverterService.delete_currency"
    )
    def test_delete_currency_endpoint_raises_unexpected_error(
        self, mock_delete_repository: Mock
    ):

        mock_delete_repository.side_effect = Exception("test error")
        payload = Currency(acronym="TEST", name="TESTE-NAME", dolar_price_reference=10)

        with self.assertRaises(GenericApiException) as context_error:
            delete_currency_by_acronym(payload.acronym)
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertEqual(
            context_error.exception.detail, {"error": "Some error ocurred!"}
        )

    @patch("app.repositories.mongo_repository.MongoRepository.delete_by_acronym")
    def test_delete_currency_by_acronym(self, mock_repository_delete_by_acronym: Mock):
        mock_repository_delete_by_acronym.return_value = None

        response: JSONResponse = delete_currency_by_acronym(acronym="USD")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.body), {"acronym": "USD"})

    @patch("app.repositories.mongo_repository.MongoRepository.delete_by_acronym")
    def test_delete_currency_by_acronym_and_repository_raises_unexpected_error(
        self, mock_repository_delete: Mock
    ):

        mock_repository_delete.side_effect = Exception("test error")

        with self.assertRaises(CurrencyServiceException) as context_error:
            delete_currency_by_acronym(acronym="USD")
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertEqual(
            context_error.exception.detail, {"error": "Error to delete currency"}
        )

    @patch(
        (
            "app.api.v1.currency_converter.service.CurrencyConverterService."
            "delete_currency"
        )
    )
    def test_delete_currency_by_acronym_and_flow_raises_unexpected_error(
        self, mock_delete_currency_by_name: Mock
    ):

        mock_delete_currency_by_name.side_effect = Exception("test error")

        with self.assertRaises(GenericApiException) as context_error:
            delete_currency_by_acronym(acronym="USD")
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertEqual(
            context_error.exception.detail, {"error": "Some error ocurred!"}
        )
