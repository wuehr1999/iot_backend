#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

from sqlmodel import Field, Session, SQLModel, create_engine, select

class Level(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    dev_id: str
    backend_timestamp: int 
    accquisition_timestamp: int 
    meter: float 
