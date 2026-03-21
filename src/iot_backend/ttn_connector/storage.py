#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

import click
import subprocess
import json
import re
import time
from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select

import iot_backend.types.temperature as temp
import iot_backend.postgres_connector.postgres_connector as pg

def pull(application: str, key: str, interval: int):
    cmd = [ "curl" ]
    cmd += [
        "-G", f"https://eu1.cloud.thethings.network/api/v3/as/applications/{application}/packages/storage/uplink_message",
        "--header", f"Authorization: Bearer {key}",
        "--header", "Accept: text/event-stream",
        "-d", f"last={interval}s",
        "-d", "field_mask=up.uplink_message.decoded_payload",
    ]
    call = subprocess.run(cmd, shell = False, check = True, capture_output = True)
    payload = call.stdout
    return list(map(json.loads, re.sub(r'\n+', '\n', payload.decode()).splitlines()))

@click.command()
@click.option("--application", required = True, type = str, help = "Name of the TTN application")
@click.option("--key", required = True, type = str, help = "API key")
@click.option("--interval", default = 30, help = "Update interval in seconds")
@click.option("--host", default = "0.0.0.0", help = "Host IP address")
def main(application: str, key: str, interval: int, host: str):

    db = pg.PostgresConnector()

    last_euis = []   
    
    while True:
        data = pull(application, key, interval + 5)
        print(data)
        euis = []
        for d in data:
            eui = d['result']['end_device_ids']['device_id']
            euis.append(eui)
            if not eui in last_euis:
                t = temp.Temperature(dev_id = eui,
                    celsius = d['result']['uplink_message']['decoded_payload']['temperature'],
                    backend_timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))         
                with Session(db.engine) as session:
                    session.add(t)
                    session.commit()
        last_euis = euis
        time.sleep(interval)
