#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
## Copyrights Frédéric Rodrigo 2011-2015                                 ##
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
from .Analyser_Osmosis import Analyser_Osmosis
from modules.Stablehash import stablehash64

sql20 = """
CREATE TEMP TABLE bnodes AS
SELECT
    id, -- needed for 'touched' view
    type_id,
    ST_PointN(ST_ExteriorRing(poly_proj), generate_series(1, npoints)) AS point_proj
FROM
    buildings
WHERE
    NOT layer AND
    wall
"""

sql21 = """
CREATE INDEX bnodes_point_proj ON bnodes USING GIST(point_proj);
"""

sql30 = """
CREATE TEMP TABLE intersection_{0}_{1} AS
SELECT
    b1.type_id AS id1,
    b2.type_id AS id2,
    ST_AsText(ST_Transform(ST_Centroid(ST_Intersection(b1.poly_proj, b2.poly_proj)), 4326)),
    ST_Area(ST_Intersection(b1.poly_proj, b2.poly_proj)) AS intersectionArea,
    least(b1.area, b2.area) * 0.10 AS threshold,
    b1.poly_proj
FROM
    {0}buildings AS b1
    JOIN {1}buildings AS b2 ON
        b1.type_id > b2.type_id AND
        b1.poly && b2.poly AND
        ST_IsValid(ST_Intersection(b1.poly_proj, b2.poly_proj)) AND
        ST_Area(ST_Intersection(b1.poly_proj, b2.poly_proj)) > 0
WHERE
    b1.wall AND
    b2.wall AND
    NOT b1.layer AND
    NOT b2.layer
"""

sql31 = """
SELECT
    *
FROM
    intersection_{0}_{1}
"""

sql40 = """
SELECT
    type_id,
    ST_AsText(ST_Transform(ST_Centroid(poly_proj), 4326))
FROM
    {0}buildings
WHERE
    NOT layer AND
    wall AND
    area < 0.5 * 0.5
"""

sql50 = """
SELECT
    DISTINCT ON (bnodes.type_id)
    buildings.type_id,
    bnodes.type_id,
    ST_AsText(ST_Transform(bnodes.point_proj, 4326))
FROM
    {0}buildings AS buildings
    JOIN {1}bnodes AS bnodes ON
        buildings.type_id > bnodes.type_id AND
        -- Help planner to use index, both ST_Expand to let planner choose
        ST_Expand(buildings.poly_proj, 0.01) && bnodes.point_proj AND
        ST_Expand(bnodes.point_proj, 0.01) && buildings.poly_proj AND
        ST_Expand(bnodes.point_proj, 0.01) && buildings.poly_proj AND
        ST_DWithin(buildings.poly_proj, bnodes.point_proj, 0.01) AND
        ST_Disjoint(buildings.poly_proj, bnodes.point_proj)
WHERE
    NOT buildings.layer AND
    buildings.wall
ORDER BY
    bnodes.type_id
"""

sql60 = """
SELECT
    ST_AsText(ST_Transform(ST_Centroid(geom), 4326)),
    ST_Area(geom)
FROM
    (
    SELECT
        (ST_Dump(ST_Union(ST_Buffer(poly_proj, 200, 'quad_segs=2')))).geom AS geom
    FROM
        intersection_{0}_{1}
    WHERE
        intersectionArea > threshold
    ) AS buffer
WHERE
    ST_Area(geom) > 1000 * 1000
"""

sql70 = """
SELECT
   DISTINCT ON (b2.type_id)
   b2.type_id,
   b1.type_id,
   ST_AsText(polygon_locate(b2.poly))
FROM
   {0}buildings AS b1
   JOIN {1}buildings AS b2 ON
       b2.type_id != b1.type_id AND
       b1.tags->'building' = b2.tags->'building' AND
       b1.wall = b2.wall AND
       ST_Intersects(b1.poly_proj, b2.poly_proj) AND
       ST_Dimension(ST_Intersection(b1.poly_proj, b2.poly_proj)) > 0 AND
       b2.npoints = 4
WHERE
   NOT b1.layer AND
   NOT b2.layer
ORDER BY
   b2.type_id
"""

class Analyser_Osmosis_Building_Overlaps(Analyser_Osmosis):

    requires_tables_full = ['buildings']
    requires_tables_diff = ['buildings', 'touched_buildings', 'not_touched_buildings']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.FR = config.options and ("country" in config.options and config.options["country"].startswith("FR") or "test" in config.options)
        fix = T_(
'''Fix geometry so that buildings don't overlap, but share nodes if physically joined.
If geometry is correct and there's some vertical difference then make use of the `layer` tag to indicate this.''')

        self.classs_change[1] = self.def_class(item = 0, level = 3, tags = ['building', 'geom', 'fix:chair'],
            title = T_('Building intersection'),
            fix = fix)
        self.classs_change[2] = self.def_class(item = 0, level = 2, tags = ['building', 'geom', 'fix:chair'],
            title = T_('Large building intersection'),
            fix = self.merge_doc(fix, T_(
'''Large intersections may also be duplicates - in which case you should delete the less accurate elements.''')))
        self.classs_change[3] = self.def_class(item = 0, level = 3, tags = ['building', 'geom', 'fix:chair'],
            title = T_('Building too small'),
            detail = T_('The area of this feature is too small to possibly be a building.'),
            fix = T_(
'''- Correct the geometry if inaccurately mapped.
- Correct the tagging if this isn't a building.
- Delete the feature if it's invalid.'''))
        self.classs_change[4] = self.def_class(item = 0, level = 3, tags = ['building', 'geom', 'fix:chair'],
            title = T_('Gap between buildings'),
            detail = T_(
'''It looks like these buildings should be physically joined, but they don't share nodes to indicate this.'''),
            fix = T_('Connect the buildings by joining nodes where appropriate.'))
        self.classs_change[5] = self.def_class(item = 0, level = 1, tags = ['building', 'fix:chair'],
            title = T_('Large building intersection cluster'),
            fix = self.merge_doc(fix, T_(
'''Large intersections may also be duplicates - in which case you should delete the less accurate elements.''')))
        if self.FR:
            self.classs_change[6] = self.def_class(item = 1, level = 3, tags = ['building', 'geom', 'fix:chair'],
                title = T_("Building in parts"),
                fix = T_('Merge the building parts together as appropriate.'))

        self.callback30 = lambda res: {"class":2 if res[3] > res[4] else 1, "data":[self.any_id, self.any_id, self.positionAsText]}
        self.callback40 = lambda res: {"class":3, "data":[self.any_full, self.positionAsText]}
        self.callback50 = lambda res: {"class":4, "data":[self.any_id, self.any_id, self.positionAsText]}
        self.callback60 = lambda res: {"class":5, "subclass": stablehash64(res[0]), "data":[self.positionAsText]}
        if self.FR:
            self.callback70 = lambda res: {"class":6, "data":[self.any_id, self.any_id, self.positionAsText]}

    def analyser_osmosis_full(self):
        self.run(sql20)
        self.run(sql21)
        self.run(sql30.format("", ""))
        self.run(sql31.format("", ""), self.callback30)
        self.run(sql40.format(""), self.callback40)
        self.run(sql50.format("", ""), self.callback50)
        self.run(sql60.format("", ""), self.callback60)
        if self.FR:
            self.run(sql70.format("", ""), self.callback70)

    def analyser_osmosis_diff(self):
        self.run(sql20)
        self.run(sql21)
        self.create_view_touched("bnodes", ["W", "R"])
        self.run(sql30.format("touched_", ""))
        self.run(sql30.format("not_touched_", "touched_"))
        self.run(sql31.format("touched_", ""), self.callback30)
        self.run(sql31.format("not_touched_", "touched_"), self.callback30)
        self.run(sql40.format("touched_"), self.callback40)
        self.run(sql50.format("touched_", ""), self.callback50)
        self.run(sql50.format("not_touched_", "touched_"), self.callback50)
        #self.run(sql60.format("", ""), self.callback60) Can be done in diff mode without runing a full sql30
        if self.FR:
            self.run(sql70.format("touched_", ""), self.callback70)
            self.run(sql70.format("not_touched_", "touched_"), self.callback70)
