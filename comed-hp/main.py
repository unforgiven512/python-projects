#!/usr/bin/env python3

import os
import sys
import time
import datetime
import logging
import math
import requests
import json
import sqlite3
import struct
import numpy as np
import sched
import paho.mqtt.client as mqttClient


s = sched.scheduler(time.time, time.sleep)
td = datetime.date.today()

base_url = 'https://hourlypricing.comed.com/api?type='
url_curhour = base_url + 'currenthouraverage'
url_fivemin = base_url + '5minutefeed'

update_interval_sec = 60

mqtt_connected = False
mqtt_broker = "mqtt.kd9qzo.net"


def get_current_hour_average_price() -> tuple:
    resp = requests.get(url_curhour)
    data = json.loads(resp.content)
    for x in data:
        millis_utc = int(x['millisUTC'])
        price = float(x['price'])
    utc = millis_utc / 1000
    local_dt = datetime.datetime.fromtimestamp(utc)

    return (utc, local_dt, price)


def print_current_price_info(price_datetime: datetime.datetime, price_value_cents: float, additional_text: str=''):
    print("%s\t\t$%.03f%s" % (price_datetime.strftime("%Y-%m-%d %H:%M:%S"), (price_value_cents / 100.0), additional_text))


def main():
    print("===== ComEd Hourly Pricing API Demo (ver: %04d-%02d-%02d) =====\n\n" % (td.year, td.month, td.day))
    iterations = 0
    previous_price = 0.0

    while True:
        try:
            iterations += 1
            price_utc, price_local_dt, price_value = get_current_hour_average_price()
            if previous_price < price_value:
                price_change = "\t(the price went UP)"
            elif previous_price > price_value:
                price_change = "\t(the price went DOWN)"
            elif previous_price == price_value:
                price_change = "\t(the price did not change)"
            else:
                price_change = "\t(something weird happened)"

            previous_price = price_value
            print_current_price_info(price_local_dt, price_value, price_change)
            time.sleep(update_interval_sec)
        except KeyboardInterrupt:
            print("Interrupted by keyboard exception; exiting after %d iterations..." % (iterations))
            exit(0)


if __name__ == '__main__':
    main()
