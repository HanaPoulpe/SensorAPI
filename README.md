# Sensor API

![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.10,3.11&color=blue?style=flat-square&logo=python)
[![codecov](https://codecov.io/gh/HanaPoulpe/SensorAPI/branch/master/graph/badge.svg?token=OA8EN7TRSS)](https://codecov.io/gh/HanaPoulpe/SensorAPI)

A Python/Flask Rest API for Sensor data updating.

## API Reference:

* /api
  * /metric: [```PUT```](#api_metric_put) [```GET```](#api_metri_get)
    * /list: [```GET```](#api_metric_list)

### <a id="api_metric_put"></a>Sending metrics:

You can send new metrics using: ```/api/metric``` ```PUT``` method.

````json
{
  "api_key": "EXAMPLE_KEY_123",
  "sensor_id": "sensor_name_123",
  "metrics": {
    "metric_name": {
      "timestamp": "2022-01-16T10:14:18.055879",
      "value": 123.456
    }
  }
}
````

* ```api_key``` **mandatory**: Access key matching the sensor.
* ````sensor_key```` **mandatory**: Sensor key
* ````metrics```` **mandatory**: list of metric definitions
  * ````metric_name```` **at least 1**: Name of the metric, must match ```r"[A-Za-z0-9][A-Za-z0-9._-]+[A-Za-z0-9]"```
    * ````timestamp````: Date/Time of the metric matching ISO-8601 format. If not provided, current UTC time will be used.
    * ````value````: Value as number.

**Returns:**

````json
{
  "status_code": 200,
  "error": {
    "code": 123,
    "message": "error message"
  }
}
````

* ````status_code````: HTTP Status code
* ````error````: If an error occurred, this is the error definition.
  * ````code````: Error code
    * 400: Request had invalid syntax
    * 401: Credentials are invalid
    * 511: Network authentication required
