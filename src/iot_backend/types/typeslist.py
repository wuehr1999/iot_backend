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
# File: typeslist.py
# ------------------------------------------------------------------------
# Description: List of datatypes
# ------------------------------------------------------------------------
# Created: 04.04.2026 
# ------------------------------------------------------------------------
# Last Modified: 05.04.2026 
# ------------------------------------------------------------------------
# MIT License
# ------------------------------------------------------------------------

class TypesList:
    TEMPERATURE = 0
    LEVEL       = 1
    POSITION    = 2

    def __init__(self):
        pass

    def from_name(self, name: str) -> int | None:
        if "temperature" in name:
            return TypesList.TEMPERATURE
        elif "level" in name:
            return TypesList.LEVEL
        elif "position" in name:
            return TypesList.POSITION
        else:
            return None

    def from_name_list(self, names: list[str]) -> list[int | None]:
        typelist: list[int | None] = []
        for n in names:
            typelist.append(self.from_name(n))
        return typelist

