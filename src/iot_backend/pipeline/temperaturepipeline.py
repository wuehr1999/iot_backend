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
# File: temperaturepipeline.py
# ------------------------------------------------------------------------
# Description: Temperature pipeline using TTN mass storage to postgres
# ------------------------------------------------------------------------
# Created: 04.04.2026 
# ------------------------------------------------------------------------
# Last Modified: 04.04.2026 
# ------------------------------------------------------------------------
# MIT License
# ------------------------------------------------------------------------

import iot_backend.pipeline.pipeline as pipeline
import iot_backend.types.typeslist as typeslist
import iot_backend.filters.filter_ttn_mass_storage as ttnfilter
import iot_backend.filters.filter_postgresdb as dbfilter

import click
import time

@click.command()
@click.option("--application", required = True, type = str, help = "Name of the TTN application")
@click.option("--key", required = True, type = str, help = "API key")
@click.option("--interval", default = 30, help = "Update interval in seconds")
@click.option("--dev_id", required = True, help = "Default Sensor EUI")
def main(application: str, key: str, interval: int, dev_id: str):
    pipeline_temp = pipeline.Pipeline([typeslist.TypesList.TEMPERATURE])

    fil_ttn = ttnfilter.TtnMassStorageFilter("ttnfilter", dev_id, [typeslist.TypesList.TEMPERATURE], application, key, interval, True)
    pipeline_temp.register(fil_ttn)

    fil_db = dbfilter.PostgresDbFilter("dbfilter")
    pipeline_temp.register(fil_db)

    while True:
        pipeline_temp.spin()
        time.sleep(0.5)
