import json

from fastapi import status
from fastapi.responses import JSONResponse

from app.api.v1.api_health import check_health
from tests.unit import DefaultTestCase


class HealthCheckTestCase(DefaultTestCase):

    def setUp(self) -> None:
        self.health_check_response = {"status": "OK"}
        self.health_check_status_code = status.HTTP_200_OK
        return super().setUp()

    def test_health_check(self):
        response = check_health()
        self.assertTrue(isinstance(response, JSONResponse))
        self.assertTrue(status.HTTP_200_OK == self.health_check_status_code)
        self.assertEqual(json.loads(response.body), self.health_check_response)
