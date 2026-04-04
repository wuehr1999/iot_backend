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
# File: filter_postgresdb.py
# ------------------------------------------------------------------------
# Description: Postgres inserter
# ------------------------------------------------------------------------
# Created: 04.04.2026 
# ------------------------------------------------------------------------
# Last Modified: 04.04.2026 
# ------------------------------------------------------------------------
# MIT License
# ------------------------------------------------------------------------

import iot_backend.types.temperature as temp
import iot_backend.types.level as level 
import iot_backend.types.position as position 
import iot_backend.types.typeslist as typeslist
import iot_backend.filters.base.filter as filter_base
import iot_backend.postgres_connector.postgres_connector as postgres_connector
import iot_backend.types.metadata_wrapper as metadata

from sqlmodel import Field, Session, SQLModel, create_engine, select
import time

class PostgresDbFilter(filter_base.Filter):

    def __init__(self, name: str,
            host: str= 'db', port: int = 5432, 
            dbname: str = 'postgres', user: str = 'postgres', password: str = 'postgres',
            debug: bool = False):
        super().__init__(name, [typeslist.TypesList.TEMPERATURE], debug)

        self._db = postgres_connector.PostgresConnector(host, port, dbname, user, password)

    def _spin_impl(self, data: metadata.MetadataWrapper | None) -> metadata.MetadataWrapper | None:
        if data is not None:
            with Session(self._db.engine) as session:
                if data.data.backend_timestamp is None:
                    data.data.backend_timestamp = int(time.time())
                if data.data.accquisition_timestamp is None:
                    data.data.accquisition_timestamp = int(time.time())
                session.add(data.data)
                session.commit()
        return data
