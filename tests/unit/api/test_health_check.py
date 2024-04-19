import json

from fastapi import status
from fastapi.responses import (
    JSONResponse,
    RedirectResponse,
)

from app.api.v1.api_health import (
    check_health,
    return_docs,
)
from tests.unit import DefaultTestCase


class HealthCheckTestCase(DefaultTestCase):

    def setUp(self) -> None:
        self.health_check_response = {"status": "OK"}
        return super().setUp()

    def test_health_check(self):
        response = check_health()
        self.assertTrue(isinstance(response, JSONResponse))
        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertEqual(json.loads(response.body), self.health_check_response)

    def test_redirect_default_route(self):
        response = return_docs()
        self.assertTrue(isinstance(response, RedirectResponse))
        self.assertTrue(response.status_code == status.HTTP_307_TEMPORARY_REDIRECT)
