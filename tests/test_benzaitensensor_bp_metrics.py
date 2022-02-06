"""Tests metrics blue print"""
import json
import typing
import unittest.mock

import flask.testing
import flask_unittest as funittest

import src.benzaitensensor as benzaitensensor
import src.benzaitensensor.helpers


class TestMetrics(funittest.AppClientTestCase):
    """Generic test for /metrics methods"""

    def create_app(self) -> typing.Union[flask.Flask, typing.Iterator[flask.Flask]]:
        """Creates Flask app"""
        return benzaitensensor.create_app()

    def test_metric_put_wrong_body_format(
        self, app: flask.Flask, client: flask.testing.Client
    ):
        """Test the case where the request body is not valid JSon"""
        for body in ["empty", '{"invalid": 1,}']:
            response = client.put("/metrics/", data=body)

            response_json = json.loads(
                "\n".join([r.decode("utf-8") for r in response.response])
            )
            self.assertEqual(response_json["status_code"], 400)
            self.assertIsInstance(response_json["error"], dict)
            self.assertEqual(response_json["error"]["code"], 400)
            self.assertIn("message", response_json["error"])
            self.assertIsInstance(response_json["error"]["message"], str)

    def test_metrics_put_invalid_body(
        self, app: flask.Flask, client: flask.testing.Client
    ):
        """Test the case where the request body is JSon, but invalid"""
        response = client.put("/metrics/", data=json.dumps({"format": "invalid"}))

        response_json = json.loads(
            "\n".join([r.decode("utf-8") for r in response.response])
        )
        self.assertEqual(response_json["status_code"], 400)
        self.assertIsInstance(response_json["error"], dict)
        self.assertEqual(response_json["error"]["code"], 400)
        self.assertIn("message", response_json["error"])
        self.assertIsInstance(response_json["error"]["message"], str)

    @unittest.mock.patch("benzaitensensor.helpers.check_authorized")
    def test_metric_put_unauthorized(
        self, app: flask.Flask, client: flask.testing.Client, mock_check_authorized
    ):
        """Test the case where the request body is valid, the authorization failed"""
        # Setup
        mock_check_authorized.return_value = False

        # Actual Tests
        response = client.put(
            "/metrics/",
            data=json.dumps(
                {
                    "api_key": "EXAMPLE_KEY_123",
                    "sensor_id": "sensor_name_123",
                    "metrics": {
                        "test_metric": {
                            "timestamp": "2022-01-16T10:14:18.055879",
                            "value": 123,
                        },
                        "test_metric2": {
                            "value": 456,
                        },
                    },
                }
            ),
        )

        response_json = json.loads(
            "\n".join([r.decode("utf-8") for r in response.response])
        )
        self.assertEqual(response_json["status_code"], 401)
        self.assertIsInstance(response_json["error"], dict)
        self.assertEqual(response_json["error"]["code"], 401)
        self.assertIn("message", response_json["error"])

    @unittest.mock.patch("benzaitensensor.helpers.check_authorized")
    def test_metric_put_authorized(
        self, app: flask.Flask, client: flask.testing.Client, mock_check_authorized
    ):
        """Test the case where the request body is valid, the authorization failed"""
        # Setup
        mock_check_authorized.return_value = True

        # Actual Tests
        response = client.put(
            "/metrics/",
            data=json.dumps(
                {
                    "api_key": "EXAMPLE_KEY_123",
                    "sensor_id": "sensor_name_123",
                    "metrics": {
                        "test_metric": {
                            "timestamp": "2022-01-16T10:14:18.055879",
                            "value": 123,
                        },
                        "test_metric2": {
                            "value": 456,
                        },
                    },
                }
            ),
        )

        response_json = json.loads(
            "\n".join([r.decode("utf-8") for r in response.response])
        )
        self.assertEqual(response_json["status_code"], 200)
        self.assertIn("metrics", response_json)


if __name__ == "__main__":
    unittest.main()
