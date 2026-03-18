#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

from fastapi import FastAPI
import uvicorn
import click
import iot_backend.postgres_connector.postgres_connector as pg
import iot_backend.types.temperature as temp


@click.command()
@click.option("--host", default = "localhost", help = "Host IP address")
def main(host: str):
   
    db = pg.PostgresConnector(host = host)
    
    app = FastAPI()

    @app.get('/temperature')
    def get_temperature():
        values = db.fetch_query("SELECT * FROM temperature")
        data = "{}"
        if len(values) > 0:
            data = '{"data":['
            for e in values:
                data += temp.Temperature(e[0], e[2], e[1], e[3]).to_json()
                data += ","
            data = data[:-1] + "]}"
        return data

    @app.delete('/temperature')
    def clear_temperature():
        db.insert_query("DELETE FROM temperature")
        return "{}"

    uvicorn.run(app, host="localhost", port=5000)
