import json
from unittest.mock import (
    Mock,
    patch,
)

from fastapi import status
from fastapi.responses import JSONResponse

from app.api.v1.words.vowel_count.exceptions import VowelCountException
from app.api.v1.words.vowel_count.models import VowelCountRequest
from app.api.v1.words.vowel_count.views import vowel_count
from app.exceptions.default_exceptions import InternalServerErrorException
from tests.unit import DefaultTestCase


class CountVowelsTestCase(DefaultTestCase):

    def setUp(self) -> None:
        self.count_vowels_request = {"words": ["batman", "robin", "coringa"]}
        self.count_vowels_response = {"batman": 2, "robin": 2, "coringa": 3}
        return super().setUp()

    def test_vowel_count_default(self):
        response = vowel_count(
            VowelCountRequest.model_validate(self.count_vowels_request)
        )
        self.assertTrue(isinstance(response, JSONResponse))
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(json.loads(response.body), self.count_vowels_response)

    def test_vowel_count(self):
        values_list = [
            "batman",
            "robin",
            "coringa",
            "supermen",
            "diana",
            "lobo",
            "lanterna verde",
        ]
        self.count_vowels_request.update({"words": values_list})
        self.count_vowels_response.update(
            {"supermen": 3, "diana": 3, "lobo": 2, "lanterna verde": 5}
        )
        response = vowel_count(
            VowelCountRequest.model_validate(self.count_vowels_request)
        )
        self.assertTrue(isinstance(response, JSONResponse))
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(json.loads(response.body), self.count_vowels_response)

    def test_vowel_count_with_invalid_payload(self):
        with self.assertRaises(InternalServerErrorException) as context_error:
            vowel_count({})

        self.assertEqual(
            context_error.exception.detail, {"error": "Some error ocurred!"}
        )
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch("app.api.v1.words.vowel_count.service.sum")
    def test_vowel_count_service_raises_a_error(self, sum_mock: Mock):
        sum_mock.side_effect = Exception("error_exception")
        with self.assertRaises(VowelCountException) as context_error:
            vowel_count(VowelCountRequest.model_validate(self.count_vowels_request))

        self.assertEqual(
            context_error.exception.detail, {"error": "Some error ocurred!"}
        )
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_400_BAD_REQUEST
        )
