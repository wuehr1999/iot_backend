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
# File: factory.py
# ------------------------------------------------------------------------
# Description: Factory for filters 
# ------------------------------------------------------------------------
# Created: 04.04.2026 
# ------------------------------------------------------------------------
# Last Modified: 04.04.2026 
# ------------------------------------------------------------------------
# MIT License
# ------------------------------------------------------------------------

import iot_backend.filters.base.filter as filter_base
import iot_backend.filters.filter_ttn_mass_storage as ttnfilter
import iot_backend.filters.filter_postgresdb as dbfilter

class FilterFactory:

    def __init__(self):
        pass

    def create(self, filtertype: str, conf: dict) -> filter_base.Filter | None:
        if "source_ttn_masstorage" == filtertype:
            return ttnfilter.TtnMassStorageFilter(conf = conf) 
        elif "sink_postresdb" == filtertype:
            return dbfilter.PostgresDbFilter(conf = conf) 
        else:
            return None
