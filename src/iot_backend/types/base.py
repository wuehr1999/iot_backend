#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

from datetime import datetime

class Base:

    def __init__(self, dev_id: str, description: str = ""):
        self._dev_id = dev_id
        self._description = description
        self._creation_timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    @property
    def dev_id(self) -> str:
        return self._dev_id

    @property
    def description(self) -> str:
        return self._description  

    @property
    def creation_timestamp(self) -> str:
        return self._creation_timestamp
    def to_json(self) -> str:
        return '{"dev_id":"' + self.dev_id\
        + '","description":"' + self.description\
        + '","backend_timestamp":"' + self.creation_timestamp + '"}'

    def create_table_sql(self, table_name: str) -> str:
        return "CREATE TABLE IF NOT EXISTS " + str(table_name)\
        + " (dev_id text, description text, backend_timestamp text)"

    def to_sql(self, table_name: str) -> str:
        return "INSERT INTO " + table_name\
        + " (dev_id, description, backend_timestamp) VALUES ('" + self.dev_id\
        + "', '" + self.description + "', '" + self.creation_timestamp + "')" 
