#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Noémie Lehuby 2019                                         ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, SourceOpenDataSoft, CSV, Load_XY, Conflate, Select, Mapping

class Analyser_Merge_Parking_FR_IDF_park_ride(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8130, id = 751, level = 3, tags = ['merge', 'parking', 'fix:imagery', 'fix:survey'],
            title = T_('P+R parking in Île-de-France not integrated'))

        self.init(
            "https://stif.opendatasoft.com/explore/dataset/parking_relais_idf/information/",
            "Parcs Relais en Île-de-France",
            CSV(SourceOpenDataSoft(
                attribution="Île-de-France Mobilités",
                url="https://stif.opendatasoft.com/explore/dataset/parking_relais_idf")),
            Load_XY("GEO POINT", "GEO POINT",
                xFunction = lambda x: x.split(",")[1],
                yFunction = lambda y: y.split(",")[0]),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {
                        "amenity": "parking",
                        "park_ride": None}),
                conflationDistance = 300,
                mapping = Mapping(
                    static1 = {"amenity": "parking", "park_ride": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {"capacity": lambda res: int(float(res["PL_PR"])) if res["PL_PR"] != "0" else None} )))
