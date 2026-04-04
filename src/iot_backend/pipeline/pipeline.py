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
# File: pipeline.py
# ------------------------------------------------------------------------
# Description: Pipeline base class 
# ------------------------------------------------------------------------
# Created: 04.04.2026 
# ------------------------------------------------------------------------
# Last Modified: 04.04.2026 
# ------------------------------------------------------------------------
# MIT License
# ------------------------------------------------------------------------

import iot_backend.types.metadata_wrapper as metadata
import iot_backend.filters.base.filter as filter_base

class Pipeline:
    def __init__(self, sensitivity_list: list[int]):
        self._sensitivity_list = sensitivity_list
        self._filters: list[filter_base.Filter] = []        

    def register(self, fil: filter_base.Filter):
        for s in self._sensitivity_list:
            if fil.is_compatible(s):
                self._filters.append(fil)
            else:
                raise RuntimeError("Type ist not compatible with input filter " + str(fil.name) + ".")

    def spin(self):
        data = None
        for f in self._filters:
            data = f.spin(data)
            if f.debug:
                print(data)
