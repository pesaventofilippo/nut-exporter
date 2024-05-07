import uvicorn
from utils import parse_key, env
from nut_client import NUTClient
import prometheus_client as prom
from fastapi import FastAPI, Response

app = FastAPI()
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


@app.get("/metrics")
def get_metrics():
    update_metrics()
    return Response(
        content=prom.generate_latest(),
        media_type="text/plain"
    )


if __name__ == "__main__":
    prom.disable_created_metrics()
    prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
    prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
    prom.REGISTRY.unregister(prom.GC_COLLECTOR)

    update_metrics()
    uvicorn.run(app, host="0.0.0.0", port=env.PROMETHEUS_PORT)
