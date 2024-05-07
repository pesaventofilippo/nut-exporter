from PyNUTClient.PyNUT import PyNUTClient


class NUTClient:
    ALL_FLAGS = ["BYPASS", "CAL", "CHRG", "DISCHRG", "FSD", "LB", "OB", "OL", "RB", "SD"]

    def __init__(self, host: str, port: int, ups_name: str, username: str=None, password: str=None, timeout: int=5):
        self.host = host
        self.port = port
        self.ups_name = ups_name
        self.username = username
        self.password = password
        self.timeout = timeout

        self._nut: PyNUTClient = None
        self._connect()

    def _connect(self):
        self._nut = PyNUTClient(host=self.host, port=self.port,
                               login=self.username, password=self.password,
                               timeout=self.timeout)
        if (self.username is not None) and (self.password is not None):
            self._nut.DeviceLogin(self.ups_name)

    def _get_raw_data(self) -> dict[bytes, bytes]:
        try:
            data = self._nut.GetUPSVars(self.ups_name)
        except (EOFError, AttributeError):
            self._connect()
            data = self._nut.GetUPSVars(self.ups_name)
        return data

    def get_data(self) -> dict[str, float|dict]:
        raw_data = self._get_raw_data()
        data = {}
        flags = []

        for key, value in raw_data.items():
            key = key.decode()
            value = value.decode()

            if key == "ups.status":
                flags = value.split(" ")

            elif value in ["yes", "true", "active", "enabled"]:
                data[key] = 1
            elif value in ["no", "false", "inactive", "disabled"]:
                data[key] = 0
            else:
                try:
                    data[key] = float(value)
                except ValueError:
                    pass

        data["ups.status"] = {flag: 1 if flag in flags else 0 for flag in self.ALL_FLAGS}
        return data
