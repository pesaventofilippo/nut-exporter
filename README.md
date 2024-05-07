# nut-exporter
Yet Another Prometheus NUT Exporter

### Description
This is a very basic Prometheus exporter for [NUT (Network UPS Tools)](https://networkupstools.org) that exports readable values from the UPS.  
It is intended to be used with a NUT server that is already set up and running.

## Usage
The exporter is configured using environment variables.  
Every variable has a default value, so you can just run the exporter without setting any of them, if you want.

| Variable            | Description                                            | Default       |
|---------------------|--------------------------------------------------------|---------------|
| `PROMETHEUS_PORT`   | The port the exporter listens on                       | `8000`        |
| `PROMETHEUS_PREFIX` | The prefix for the Prometheus metrics                  | `"nut"`       |
| `NUT_HOST`          | The address of the NUT server                          | `"localhost"` |
| `NUT_PORT`          | The port of the NUT server                             | `3493`        |
| `UPS_NAME`          | The name of the UPS to monitor                         | `"ups"`       |
| `NUT_USERNAME`      | The username for the NUT server                        | `None`        |
| `NUT_PASSWORD`      | The password for the NUT server                        | `None`        |
| `NUT_TIMEOUT`       | The timeout for the NUT server connection (in seconds) | `5`           |
