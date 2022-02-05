"""Metrics hook for benzaitensensord api"""
import dataclasses
import datetime
import json
import logging
import typing

import dateutil.parser
import flask

import benzaitensensor
import benzaitensensor.helpers as helpers

blue_print = flask.Blueprint(
    "metrics",
    "benzaitensensord",
    url_prefix="/metrics",
)


@blue_print.route("/", methods=("GET", "PUT"))
def metrics_base() -> typing.Tuple[str, int]:
    """
    API Path: /metrics

    Base metric manipulations
    It will call the specifics functions for each method

    :return: Response Body
    """
    match flask.request.method:
        case "PUT":
            return metrics_put(flask.request)
        # case "GET":
        #     return metrics_get(flask.request)
        case m:
            return response(
                http_code=405,
                error_message=f"Method {m} not supported for metrics",
            )


def response(*, http_code: int,
             error_message: str | None = None,
             error_code: int | None = None,
             **kwargs) -> typing.Tuple[str, int]:
    """
    Create response body from http code, error message/code

    :param http_code: HTTP return code
    :param error_message: Error message
    :param error_code: Error code
    :return: response body, HTTP Code
    :rtype:
    """
    return_body = kwargs

    match http_code, error_code, error_message:
        case 200, None, None:
            pass
        # case hc, ec, None:
        #     http_code = hc if 400 <= hc <= 599 else 400
        #     return_body["error"] = {
        #         "code": ec,
        #         "message": f"Undocumented error {ec}",
        #     }
        case hc, None, em:
            http_code = hc if 400 <= hc <= 599 else 400
            return_body["error"] = {
                "code": hc,
                "message": em,
            }
        # case hc, ec, em:
        #     http_code = hc if 400 <= hc <= 599 else 400
        #     return_body["error"] = {
        #         "code": ec,
        #         "message": em,
        #     }

    return_body["status_code"] = http_code
    return json.dumps(return_body), http_code


# PUT Request

@dataclasses.dataclass
class PutRequest:
    """
    Put request definition

    ATM: does nothing
    """

    @dataclasses.dataclass(frozen=True)
    class MetricValue:
        """Metric Value definition"""

        value: float
        timestamp: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.utcnow)

        def to_dict(self) -> dict[str, str]:
            """Convert value into a dict"""
            return {
                "value": self.value,
                "timestamp": self.timestamp.isoformat(),
            }

    api_key: str
    sensor_id: str
    metrics: dict[str, MetricValue]

    def __post_init__(self):
        for k, v in self.metrics.items():
            if "timestamp" in v:
                v["timestamp"] = dateutil.parser.parse(v["timestamp"])  # type: ignore

            self.metrics[k] = PutRequest.MetricValue(**v)  # type: ignore


def metrics_put(request: flask.Request) -> typing.Tuple[str, int]:
    """
    Stores new metrics values.

    ATM: Does Nothing

    :param request: Flask request
    :return: Return body, http code
    """
    # Get application configuration
    conf = benzaitensensor.ApplicationConfiguration()
    logger: logging.Logger = conf.get("logger")

    # Try loading request
    client_address = request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr)
    request_json = request.get_json(force=True, silent=True)
    if not request_json:
        logger.error("Invalid JSon request.")
        return response(
            http_code=400,
            error_message="Invalid JSon request.",
        )
    try:
        request = PutRequest(**request_json)
    except TypeError as err:
        # On JSon error
        logger.error(f"Invalid JSon Object: {request_json!r}")
        return response(
            http_code=400,
            error_message=f"Request body is not matching expected format: {err!r}",
        )
    logger.info(f"metric PUT request from {client_address}: {request!r}")

    # Checks permission
    if not helpers.check_authorized(request.api_key, request.sensor_id, "PUT", client_address):
        return response(
            http_code=401,
            error_message="Permission to put metrics denied...",
        )

    return response(
        http_code=200,
        metrics={k: v.to_dict() for k, v in request.metrics.items()},
    )
