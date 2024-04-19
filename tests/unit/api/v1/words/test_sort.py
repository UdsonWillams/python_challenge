import json

from fastapi import status
from fastapi.responses import JSONResponse

from app.api.v1.words.sort.exceptions import SortWordsException
from app.api.v1.words.sort.models import SortWordsRequest
from app.api.v1.words.sort.views import sort_words
from tests.unit import DefaultTestCase


class SortWordsTestCase(DefaultTestCase):

    def setUp(self) -> None:
        self.sort_words_asc_request = {
            "words": ["batman", "robin", "coringa"],
            "order": "asc",
        }
        self.sort_words_desc_request = {
            "words": ["batman", "robin", "coringa"],
            "order": "desc",
        }
        self.sort_words_asc_response = ["batman", "coringa", "robin"]
        self.sort_words_desc_response = ["robin", "coringa", "batman"]
        return super().setUp()

    def test_sort_words_asc_order(self):
        response = sort_words(
            SortWordsRequest.model_validate(self.sort_words_asc_request)
        )
        self.assertTrue(isinstance(response, JSONResponse))
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(json.loads(response.body), self.sort_words_asc_response)

    def test_sort_words_desc_order(self):
        response = sort_words(
            SortWordsRequest.model_validate(self.sort_words_desc_request)
        )
        self.assertTrue(isinstance(response, JSONResponse))
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(json.loads(response.body), self.sort_words_desc_response)

    def test_sort_words_invalid_order_return_the_same_value(self):
        invalid_order = {
            "words": ["batman", "robin", "coringa"],
            "order": "test",
        }
        response = sort_words(SortWordsRequest.model_validate(invalid_order))
        self.assertTrue(isinstance(response, JSONResponse))
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(json.loads(response.body), invalid_order.get("words"))

    def test_sort_words_with_invalid_payload(self):
        with self.assertRaises(SortWordsException) as context_error:
            sort_words({})

        self.assertEqual(
            context_error.exception.detail, {"error": "Some error ocurred!"}
        )
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            context_error.exception.status_code, status.HTTP_400_BAD_REQUEST
        )
