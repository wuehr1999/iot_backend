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
# File: pipeline_orchestrator.py
# ------------------------------------------------------------------------
# Description: Create pipelines from database or json
# ------------------------------------------------------------------------
# Created: 05.04.2026 
# ------------------------------------------------------------------------
# Last Modified: 05.04.2026 
# ------------------------------------------------------------------------
# MIT License
# ------------------------------------------------------------------------

import iot_backend.pipeline.pipeline as pipeline
import iot_backend.filters.base.factory as filter_factory
import iot_backend.postgres_connector.postgres_connector as pg
import iot_backend.types.typeslist as typeslist

from sqlmodel import Column, Field, Session, SQLModel, create_engine, select, JSON
import json
import time

class PipelineDescriptor(SQLModel, table = True):
    name: str = Field(primary_key = True)
    description: dict = Field(default_factory=dict, sa_column=Column(JSON))

class PipelineOrchestrator:
    SPIN_DELAY = 0.1

    def __init__(self, host: str= 'db', 
                 port: int = 5432, 
                 dbname: str = 'postgres', 
                 user: str = 'postgres', password: str = 'postgres') -> None:
         
        self._db = pg.PostgresConnector(host, port, dbname, user, password)
        self._pipelines: list[pipeline.Pipeline] = []
        self._filter_factory = filter_factory.FilterFactory()
        with Session(self._db.engine) as session:
            statement = select(PipelineDescriptor)
            descriptors = list(session.exec(statement).all())
            for d in descriptors:
                self.register(d, update_db = False)
        
    def register(self, descriptor: PipelineDescriptor, update_db: bool = True) -> None:
        tl = typeslist.TypesList()
        pl = pipeline.Pipeline(descriptor.name, descriptor.description['description'], 
            tl.from_name_list(descriptor.description['sensitivity_list']))
        for f in descriptor.description['filters']:
            pl.register(self._filter_factory.create(f['name'], f))
        for i in range(0, len(self._pipelines)):
            if descriptor.name == self._pipelines[i].name:
                self._pipelines.pop(i)
        self._pipelines.append(pl)
        if update_db:
            with Session(self._db.engine) as session:
                try: 
                    desc = session.get(PipelineDescriptor, descriptor.name)
                    session.delete(desc)
                    session.commit()
                except:
                    pass
                try:
                    session.add(descriptor)
                    session.commit()
                except:
                    pass

    def spin(self):
        while True:
            for pl in self._pipelines:
                    pl.spin()
            time.sleep(self.SPIN_DELAY)
