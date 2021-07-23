import os

import requests
from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin


def get_data():
    d = lambda x: x["data"]["result"][0]["value"][1]
    temp = requests.get(f"{getPrometheusServerUrl()}/api/v1/query", params={"query": "temperature{}"}).json()
    humidity = requests.get(f"{getPrometheusServerUrl()}/api/v1/query", params={"query": "humidity{}"}).json()
    rssi = requests.get(f"{getPrometheusServerUrl()}/api/v1/query", params={"query": "rssi{}"}).json()
    voltage = requests.get(f"{getPrometheusServerUrl()}/api/v1/query", params={"query": "voltage{}"}).json()
    return {
        "temperature": float(d(temp)),
        "humidity": float(d(humidity)),
        "rssi": float(d(rssi)),
        "voltage": float(d(voltage))
    }


def getPrometheusServerUrl():
    env_var = os.getenv("PROMETHEUS_SERVER_URL")
    if env_var is not None:
        return env_var
    else:
        raise ValueError


app = Flask(__name__, static_url_path='')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/sensor/data')
@cross_origin()
def get_d():
    return get_data()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
