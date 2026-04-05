#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

# ------------------------------------------------------------------------
#  _       _                 _  __ _
# (_)     | |               (_)/ _(_)
#  _  ___ | |_   _   _ _ __  _| |_ _  ___ _ __
# | |/ _ \| __| | | | | '_ \| |  _| |/ _ \ '__|
# | | (_) | |_  | |_| | | | | | | | |  __/ |
# |_|\___/ \__|  \__,_|_| |_|_|_| |_|\___|_|
# ------------------------------------------------------------------------
# File: filter_ttn_mass_storage.py
# ------------------------------------------------------------------------
# Description: TTN mass storage mirror
# ------------------------------------------------------------------------
# Created: 04.04.2026 
# ------------------------------------------------------------------------
# Last Modified: 04.04.2026 
# ------------------------------------------------------------------------
# MIT License
# ------------------------------------------------------------------------

import iot_backend.types.temperature as temp
import iot_backend.types.level as level 
import iot_backend.types.position as position 
import iot_backend.types.typeslist as typeslist
import iot_backend.types.metadata_wrapper as metadata
import iot_backend.filters.base.filter as filter_base

import click
import subprocess
import json
import re
import time
from datetime import datetime

class TtnMassStorageFilter(filter_base.Filter):
    POLL_OVERHEAD: int = 5

    def __init__(self, conf: dict) -> None:
        tl = typeslist.TypesList()
        self.__init_int__(name = conf['name'],
                      dev_id = conf['dev_id'],
                      sensitivity_list = tl.from_name_list(conf['sensitivity_list']),
                      application = conf['application'],
                      key = conf['key'],
                      interval = conf['interval'],
                      debug = conf['debug'])

    def __init_int__(self, name: str, dev_id: str, sensitivity_list: list[int],
                 application: str, key: str, interval: int, debug: bool = False):
        super().__init_int__(name, [typeslist.TypesList.TEMPERATURE], debug)
        self._dev_id = dev_id
        self._sensitivity_list = sensitivity_list
        for s in self._sensitivity_list:
            if not self.is_compatible(s):
                raise RuntimeError("Type ist not compatible with input filter.")
        self._application = application
        self._key = key
        self._interval = interval
        self._last_stamp = 0
        self._last_euis = []

    def _pull(self):
        interval = self._interval + self.POLL_OVERHEAD
        cmd = [ "curl" ]
        cmd += [
            "-G", f"https://eu1.cloud.thethings.network/api/v3/as/applications/{self._application}/packages/storage/uplink_message",
            "--header", f"Authorization: Bearer {self._key}",
            "--header", "Accept: text/event-stream",
            "-d", f"last={interval}s",
            "-d", "field_mask=up.uplink_message.decoded_payload",
        ]
        call = subprocess.run(cmd, shell = False, check = True, capture_output = True)
        payload = call.stdout
        return list(map(json.loads, re.sub(r'\n+', '\n', payload.decode()).splitlines()))

    def _spin_impl(self, data: metadata.MetadataWrapper | None) ->  metadata.MetadataWrapper | None:
        triggered = False
        stamp = datetime.now().second
        if self._last_stamp == 0 or abs(stamp - self._last_stamp) > self._interval:
            self._last_stamp = stamp 
            data_raw = self._pull()
            if self._debug:
                print(data_raw)
            euis = []
            for d in data_raw:
                eui = d['result']['end_device_ids']['device_id']
                euis.append(eui)
                if not eui in self._last_euis and self._dev_id == eui:
                    if typeslist.TypesList.TEMPERATURE in self._sensitivity_list: 
                        try:
                            data = metadata.MetadataWrapper(None, typeslist.TypesList.TEMPERATURE)
                            data.data = temp.Temperature(dev_id = eui,
                            celsius = d['result']['uplink_message']['decoded_payload']['temperature'])       
                            triggered = True
                        except:
                            pass
            self._last_euis = euis
            if triggered:
                return data
            else:
                return None

@click.command()
@click.option("--application", required = True, type = str, help = "Name of the TTN application")
@click.option("--key", required = True, type = str, help = "API key")
@click.option("--interval", default = 30, help = "Update interval in seconds")
@click.option("--dev_id", required = True, help = "Default Sensor EUI")
@click.option("--datatype", default = 0, help = "Default Sensor Type")
def main(application: str, key: str, interval: int, dev_id: str, datatype: int):

    fil = TtnMassStorageFilter("test", dev_id, [datatype], application, key, interval, True)
    
    while True:
        data = fil.spin()
        if data is not None:
            print(data.data)
        time.sleep(0.5)
