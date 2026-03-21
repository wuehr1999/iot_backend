#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

from sqlmodel import Field, Session, SQLModel, create_engine, select

class PostgresConnector:

    def __init__(self, host: str = 'db', port: int = 5432, dbname: str = "postgres", user: str = "postgres", password: str = "postgres"):

        con_str = "postgresql://" + user + ":" + password + "@" + host + ":" + str(port) + "/" + dbname
        print("Connecting to " + con_str)
        self._engine = create_engine(con_str)
        
        SQLModel.metadata.create_all(self._engine)

    @property
    def engine(self):
        return self._engine
