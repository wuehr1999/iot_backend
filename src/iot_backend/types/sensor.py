#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

from sqlmodel import Field, Session, SQLModel, create_engine, select

class Sensor(SQLModel, table = True):
    dev_id: str = Field(primary_key = True)
    sensor_type: int
    description: str
    soc: float | None
    battery_voltage: float | None
    latitude: float | None
    longitude: float | None
