#! /usr/bin/env python3 
# -*- coding: utf-8 -*- 

import iot_backend.types.base as base

class Temperature(base.Base):

    def __init__(self, dev_id: str, backend_timestamp: str|None = None,
                 description: str = "", celsius: float = 20.0):
        super().__init__(dev_id, description)
        self._celsius = celsius
        if backend_timestamp is not None:
            self._creation_timestamp = backend_timestamp

    @property
    def celsius(self) -> float:
        return self._celsius
    
    def to_json(self) -> str:
        return '{"dev_id":"' + self.dev_id\
        + '","description":"' + self.description \
        + '","backend_timestamp":"' + self.creation_timestamp \
        + '","celsius":' + str(self.celsius) + '}'
    
    def create_table_sql(self, table_name: str = "temperature") -> str:
        return "CREATE TABLE IF NOT EXISTS " + str(table_name)\
        + " (dev_id text, description text, backend_timestamp text, celsius float)"

    def to_sql(self, table_name: str = "temperature") -> str:
        return "INSERT INTO " + table_name\
        + " (dev_id, description, backend_timestamp, celsius) VALUES ('" + self.dev_id \
        + "', '" + self.description + "', '" + self.creation_timestamp + "','"\
        + str(self.celsius) + "')" 
