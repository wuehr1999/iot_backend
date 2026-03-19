#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

import psycopg

import iot_backend.types.temperature as temp

class PostgresConnector:

    def __init__(self, host: str, port: int = 5432, dbname: str = "iot_db", user: str = "postgres", password: str = "postgres"):
        self._conn =  psycopg.connect(host = host, port = port, dbname = dbname, user = user, password = password)

    def insert_query(self, query: str) -> None:
        with self._conn.cursor() as cur:
            cur.execute(query)
        self._conn.commit()

    def store_value(self, measurement: temp.Temperature):
        self.insert_query(measurement.create_table_sql())
        self.insert_query(measurement.to_sql())

    def fetch_query(self, query: str) -> list:
        ret = []
        with self._conn.cursor() as cur:
            cur.execute(query)
            ret = cur.fetchall()
        self._conn.commit()
        return ret
