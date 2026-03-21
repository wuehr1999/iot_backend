#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

from fastapi import FastAPI
import uvicorn
import click
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete

import iot_backend.postgres_connector.postgres_connector as pg
import iot_backend.types.temperature as temp


@click.command()
@click.option("--host", default = "localhost", help = "Host IP address")
def main(host: str):
   
    db = pg.PostgresConnector(host = host)
    
    app = FastAPI()

    @app.get('/temperature')
    def get_temperature():
        with Session(db.engine) as session:
            statement = select(temp.Temperature)
            temperatures = session.exec(statement).all()
            return list(temperatures)

    @app.delete('/temperature')
    def clear_temperature():
        with Session(db.engine) as session:
            statement = delete(temp.Temperature)
            temperatures = session.exec(statement)
            session.commit()
        return "{}"

    uvicorn.run(app, host="localhost", port=5000)
