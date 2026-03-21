#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import click
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete

import iot_backend.postgres_connector.postgres_connector as pg
import iot_backend.types.temperature as temp


@click.command()
@click.option("--host", default = "0.0.0.0", help = "Host IP address")
def main(host: str):
   
    db = pg.PostgresConnector()
    
    app = FastAPI()
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get('/temperature')
    def get_temperature():
        with Session(db.engine) as session:
            statement = select(temp.Temperature.dev_id).distinct('dev_id')
            dev_ids = list(session.exec(statement).all())
            data = []
            for dev_id in dev_ids:
                statement = select(temp.Temperature.celsius).where(temp.Temperature.dev_id == dev_id) 
                temperatures = list(session.exec(statement).all())
                data.append({"dev_id": dev_id, "celsius": temperatures})
            return data

    @app.delete('/temperature')
    def clear_temperature():
        with Session(db.engine) as session:
            statement = delete(temp.Temperature)
            temperatures = session.exec(statement)
            session.commit()
        return "{}"

    uvicorn.run(app, host = host, port = 5000)
