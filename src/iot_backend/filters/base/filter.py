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
# File: filter.py
# ------------------------------------------------------------------------
# Description: Filter base implementation
# ------------------------------------------------------------------------
# Created: 04.04.2026 
# ------------------------------------------------------------------------
# Last Modified: 04.04.2026 
# ------------------------------------------------------------------------
# MIT License
# ------------------------------------------------------------------------


import json
import iot_backend.types.metadata_wrapper as metadata

class Filter:

    def __init__(self, conf_json: str,) -> None:
        conf = json.loads(conf_json)
        self.__init__(conf.name, conf.type_list, conf.type_list.debug)

    def __init__(self, name: str, type_list: list[int], debug: bool) -> None:
        self._name: str = name
        self._type_list: list[int] = type_list
        self._debug = debug

    def spin(self, data: metadata.MetadataWrapper | None = None) -> metadata.MetadataWrapper | None:
        return self._spin_impl(data)

    def _spin_impl(self, data: metadata.MetadataWrapper | None) -> metadata.MetadataWrapper | None:
        return data

    def is_compatible(self, datatype: int) -> bool:
        return datatype in self._type_list

    @property
    def name(self):
        return self._name
    
    @property
    def debug(self):
        return self._debug

