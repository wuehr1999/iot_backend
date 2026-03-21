#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

from sqlmodel import Field, Session, SQLModel, create_engine, select

class Temperature(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    celsius: int
    backend_timestamp: str
    dev_id: str
