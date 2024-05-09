import os


def parse_key(key: str) -> str:
    REPLACE_CHARS = ".- "
    for char in REPLACE_CHARS:
        key = key.replace(char, "_")
    return key.lower()


class EnvironmentConfig:
    def __init__(self):
        self.PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "8000"))
        self.PROMETHEUS_PREFIX = os.getenv("PROMETHEUS_PREFIX", "nut")
        self.NUT_HOST = os.getenv("NUT_HOST", "localhost")
        self.NUT_PORT = int(os.getenv("NUT_PORT", "3493"))
        self.UPS_NAME = os.getenv("UPS_NAME", "ups")
        self.NUT_USERNAME = os.getenv("NUT_USERNAME", None)
        self.NUT_PASSWORD = os.getenv("NUT_PASSWORD", None)
        self.NUT_TIMEOUT = int(os.getenv("NUT_TIMEOUT", "5"))
        self.DISABLE_STATIC = os.getenv("DISABLE_STATIC", "false").lower() in ["true", "1", "yes", "y"]


env = EnvironmentConfig()
