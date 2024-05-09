import prometheus_client as prom
from modules.nut_client import NUTClient
from modules.utils import parse_key, env
from http.server import HTTPServer, BaseHTTPRequestHandler

metrics: dict[str, prom.Gauge] = {}
nut = NUTClient(
    host=env.NUT_HOST,
    port=env.NUT_PORT,
    ups_name=env.UPS_NAME,
    username=env.NUT_USERNAME,
    password=env.NUT_PASSWORD,
    timeout=env.NUT_TIMEOUT
)


def set_metric(metric_name: str, value: float, original_name: str, labels: dict[str, str]=None):
    if env.DISABLE_STATIC:
        if metric_name.endswith("_nominal") \
            or metric_name.startswith("driver_") \
            or metric_name in ["device_info", "ups_productid", "ups_vendorid"]:
            return

    metric_name = f"{env.PROMETHEUS_PREFIX}_{metric_name}"
    if metric_name not in metrics:
        metrics[metric_name] = prom.Gauge(metric_name, f"NUT value {original_name}", labels.keys())
    metrics[metric_name].labels(**labels).set(value)


def update_metrics():
    data = nut.get_data()
    for key, value in data.items():
        name = parse_key(key)

        if name == "ups_status":
            for flag, flag_value in value.items():
                set_metric(name, flag_value, key, {"ups": env.UPS_NAME, "flag": flag})
        else:
            set_metric(name, value, key,{"ups": env.UPS_NAME})


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            update_metrics()

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(prom.generate_latest())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")


if __name__ == "__main__":
    prom.disable_created_metrics()
    prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
    prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
    prom.REGISTRY.unregister(prom.GC_COLLECTOR)

    server = HTTPServer(("0.0.0.0", env.PROMETHEUS_PORT), MetricsHandler)
    server.serve_forever()
