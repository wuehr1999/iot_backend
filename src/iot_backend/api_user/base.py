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
# File: base.py
# ------------------------------------------------------------------------
# Description: User API base implementation
# ------------------------------------------------------------------------
# Created: 04.04.2026 
# ------------------------------------------------------------------------
# Last Modified: 04.04.2026 
# ------------------------------------------------------------------------
# MIT License
# ------------------------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import click
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete
import threading

import iot_backend.postgres_connector.postgres_connector as pg
import iot_backend.types.temperature as temp
import iot_backend.types.level as level 
import iot_backend.types.position as position 
import iot_backend.types.typeslist as typeslist
import iot_backend.pipeline.pipeline_orchestrator as orchestrator

@click.command()
@click.option("--host", default = "0.0.0.0", help = "Host IP address")
@click.option("--dbhost", default = "db", help = "Database host IP address")
def main(host: str, dbhost: str):
   
    db = pg.PostgresConnector(dbhost)
    
    orch = orchestrator.PipelineOrchestrator(dbhost)
    orch_thread = threading.Thread(target = orch.spin)
    orch_thread.start()

    app = FastAPI()
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get('/api/v1/pipeline')
    def get_pipelines():
        with Session(db.engine) as session:
            statement = select(orchestrator.PipelineDescriptor)
            return session.exec(statement).all()
        
    @app.post('/api/v1/pipeline')
    def post_pipeline(pipelines: list[orchestrator.PipelineDescriptor]):
        with Session(db.engine) as session:
            for pl in pipelines:
                orch.register(pl)
        return pipelines

    @app.get('/api/v1/temperature')
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

    @app.delete('/api/v1/temperature')
    def clear_temperature():
        with Session(db.engine) as session:
            statement = delete(temp.Temperature)
            temperatures = session.exec(statement)
            session.commit()
        return "{}"

    uvicorn.run(app, host = host, port = 5000)
