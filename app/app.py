import os
import re


regex = "(?P<symbol>[A-Z0-9]{4})(?P<packlenght>[A-Z0-9]{4})(?P<prototype>[A-Z0-9]{4})(?P<hardtype>[A-Z0-9]{4})(?P<firmware>[A-Z0-9]{8})(?P<IMEI>[A-Z0-9]{16})(?P<RTC>[A-Z0-9]{12})(?P<reserved1>[A-Z0-9]{4})(?P<statedatalenght>[A-Z0-9]{4})(?P<alarmtype>[A-Z0-9]{2})(?P<terminalinfo>[A-Z0-9]{2})(?P<reserved2>[A-Z0-9]{4})(?P<batteryvoltage>[A-Z0-9]{4})(?P<powervoltage>[A-Z0-9]{4})(?P<taginfolenght>[A-Z0-9]{4})(?P<tagtype>[A-Z0-9]{2})(?P<tagnumber>[A-Z0-9]{2})(?P<taglenght>[A-Z0-9]{2})(?P<tagid>[A-Z0-9]{8})(?P<tagstatus>[A-Z0-9]{2})(?P<tagbatteryvoltage>[A-Z0-9]{4})(?P<tagtemperature>[A-Z0-9]{4})(?P<taghumidity>[A-Z0-9]{2})(?P<RSSI>[A-Z0-9]{2})(?P<packetindex>[A-Z0-9]{4})(?P<checkcode>[A-Z0-9]{4})(?P<stopsymbol>[A-Z0-9]{4})"

import requests
from prometheus_client import start_http_server, Gauge, Counter
import time




def to_binary(hexxx):
    return bin(int(hexxx, 16))[2:].zfill(4 * len(hexxx))


def get_temperature(hex):
    bin_data = to_binary(hex)
    ok = (bool(0) if bin_data[0] == "1" else bool(1))
    positive = bool(1) if bin_data[1] == "0" else bool(0)
    splited_bin_data = list(bin_data)
    splited_bin_data[0] = "0"
    splited_bin_data[1] = "0"
    int_in_array = list(str(int("".join(splited_bin_data), 2)))
    last = int_in_array[-1]
    int_in_array[-1] = "."
    int_in_array.append(last)
    final_temp = float("".join(int_in_array)) if positive else -float("".join(int_in_array))
    return final_temp


def get_rssi(hexa):
    return -int(hexa, 16)


def get_humidity(hexa):
    return int(hexa, 16)


def get_voltage(hexa):
    l = list(str(int(hexa, 16)))
    c = l[1:]
    for _ in c:
        l.pop(-1)
    l.append(".")
    for i in c:
        l.append(i)
    return float("".join(l))


def transform_data(data):
    cap = re.match(regex, data[1])

    data = {
        "rssi": get_rssi(cap["RSSI"]),
        "temp": get_temperature(cap["tagtemperature"]),
        "humidity": get_humidity(cap["taghumidity"]),
        "batteryvoltage": get_voltage(cap["tagbatteryvoltage"]),
        "date": res[0][2]
    }

    t.set(data["temp"])
    r.set(data["rssi"])
    h.set(data["humidity"])
    v.set(data["batteryvoltage"])


if __name__ == '__main__':
    t = Gauge("temperature", "Temperature (C)")
    r = Gauge("rssi", "RSSI (dBm)")
    h = Gauge("humidity", "Humidity (%)")
    v = Gauge("voltage", "Bettery Voltage (V)")
    start_http_server(int(os.getenv("METRICS_PORT")))
    res = requests.get("http://app.objco.com:8099/?account=16L1SPQZS3&limit=1").json()
    truc = [transform_data(i) for i in res]
    time.sleep(60 * 5)


