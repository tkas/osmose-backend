#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights osmose project 2022                                        ##
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
from plugins.Plugin import Plugin
from modules.Stablehash import stablehash64

class TagFix_Access(Plugin):
  def init(self, logger):
    Plugin.init(self, logger)

    self.suffixesNode = ["", ":conditional"]
    self.suffixesWay = []
    for d in ["", ":forward", ":backward", ":both_ways"]:
      self.suffixesWay.append(d)
      self.suffixesWay.append(d + ":conditional")
      self.suffixesWay.append(":lanes" + d)
      self.suffixesWay.append(":lanes" + d + ":conditional")

    # Note: emergency is excluded as it's also for hospital facilities
    self.accessKeys = ["4wd_only", "access", "agricultural", "atv", "bdouble", "bicycle", "boat", "bus", "canoe", "caravan", "carriage", "coach", "disabled", "dog", "foot", "golf_cart", "goods", "hazmat",
                       "hazmat:water", "hgv", "horse", "hov", "inline_skates", "light_rail", "minibus", "mofa", "moped", "motor_vehicle", "motorboat", "motorcar", "motorcycle", "motorhome", "psv",
                       "share_taxi", "ship", "ski:nordic", "ski", "small_electric_vehicle", "snowmobile", "speed_pedelec", "subway", "swimming", "tank", "taxi", "tourist_bus", "trailer", "train", "tram", "vehicle"]
    self.accessValuesGeneral = ["yes", "no", "private", "permissive", "permit", "destination", "delivery", "customers", "designated", "use_sidepath", "agricultural", "forestry", "discouraged"]
    self.accessValuesSpecial = {"bicycle": ["optional_sidepath", "dismount"],
                                "canoe": ["put_in", "portage"],
                                "dog": ["leashed", "unleashed", "outside"],
                                "horse": ["dismount"],
                                "mofa": ["dismount"],
                                "moped": ["dismount"],
                                "motorcycle": ["dismount"],
                                "speed_pedelec": ["dismount"],
                               }

    self.errors[30404] = self.def_class(item = 3040, level = 3, tags = ['highway', 'fix:chair'],
        title = T_('Uncommon access value'),
        detail = T_('''The value of the access tag is not one of the common access values: `{0}`.''', ", ".join(self.accessValuesGeneral)),
        resource="https://wiki.openstreetmap.org/wiki/Key:access",
        trap = T_('''If there is no other tag (or combination of tags) that properly describes the access permissions, custom tags may be used.'''))
    self.errors[30405] = self.def_class(item = 3040, level = 3, tags = ['highway', 'fix:chair'],
        title = T_('Transport mode in access value'),
        detail = T_('''The value of the access tag is a transport mode (such as `access=foot`). Consider replacing it with a more specific tag listing the transport mode first, for example `access=no` + `foot=yes`.'''),
        trap = T_('''Ensure that the access remains the same and does not conflict with other tags. This is especially likely if access tags are combined with directional and/or conditional access tags, or when transport modes are mixed with regular access values.'''),
        resource="https://wiki.openstreetmap.org/wiki/Key:access")

  def checkAccessKeys(self, tags, suffixes):
    err = []
    accessTags = {}
    for accesskey in self.accessKeys:
      for suffix in suffixes:
        if accesskey + suffix in tags:
          accessTags[accesskey + suffix] = {"transportMode": accesskey, "value": tags[accesskey + suffix], "suffix": suffix}

    for tag in accessTags:
        isConditional = accessTags[tag]["suffix"].endswith(":conditional")
        isLanes = "lanes" in accessTags[tag]["suffix"].split(":")
        if isLanes:
            if isConditional:
                # Too difficult, the condition itself may also contain ; and |. Just take the first value
                values = set(accessTags[tag]["value"].split("@")[0].replace("|", ";").split(";"))
            else:
                values = set(accessTags[tag]["value"].replace("|", ";").split(";"))
        else:
            values = set(accessTags[tag]["value"].split(";"))
            if isConditional:
                # Get the last value per condition. If there's no @, assume the ; was inside a condition
                values = set(map(lambda v: v.split("@", 1)[0], filter(lambda v: "@" in v, values)))

        # Remove whitespace, and remove the special values 'none' (:lanes/:conditional), 'variable' or '' (:lanes only)
        values = set(map(str.strip, values))
        if isLanes or isConditional:
            values = set(filter(lambda v: (v not in ('', 'variable', 'none') or not isLanes) and (v != 'none' or not isConditional), values))

        for accessVal in values:
            transportMode = accessTags[tag]["transportMode"]
            if transportMode in self.accessValuesSpecial and accessVal in self.accessValuesSpecial[transportMode]:
                continue
            if not accessVal in self.accessValuesGeneral:
                if (accessVal in self.accessKeys or accessVal == "emergency") and accessVal != transportMode:
                    if not isLanes:
                        propose = tag + " = ### + " + accessVal + accessTags[tag]["suffix"] + " = yes"
                        if len(values) > 1 or isConditional:
                            propose = propose.replace("###", "...") # i.e. access=bus;destination should become access=destination + bus=yes instead of access=no + bus=yes
                        else:
                            propose = propose.replace("###", "no") # assume 'no' holds for all other transport modes
                        if isConditional:
                            propose = propose + " @ (...)" # conditional may need to change
                    else:
                        # Not giving explicit fix suggestions, could be e.g. *:lanes = bus;destination|bus|yes or a *:lanes:conditional
                        propose = tag + " = ... + " + accessVal + accessTags[tag]["suffix"] + " = ..."
                    err.append({
                        "class": 30405,
                        "subclass": 0 + stablehash64(tag + '|' + accessVal),
                        "text": T_("Access value \"{0}\" for key \"{1}\" is a transport mode. Consider using \"{2}\" instead", accessVal, tag, propose)
                    })
                else:
                    err.append({
                        "class": 30404,
                        "subclass": 0 + stablehash64(tag + '|' + accessVal),
                        "text": T_("Unknown access value \"{0}\" for key \"{1}\"", accessVal, tag)
                    })

    if err != []:
        return err

  def way(self, data, tags, nds):
    return self.checkAccessKeys(tags, self.suffixesWay)

  def node(self, data, tags):
    return self.checkAccessKeys(tags, self.suffixesNode)

  def relation(self, data, tags, members):
    pass


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Access(None)
        a.init(None)

        # Valid nodes and ways
        for t in [{"amenity": "parking", "vehicle": "no"},
                  {"amenity": "parking", "vehicle:conditional": "no @ wet"},
                  {"amenity": "parking", "vehicle:conditional": "no @ (wet); none @ Su"},
                  {"access": "agricultural", "agricultural": "designated"},
                  {"agricultural": "agricultural"},
                  {"highway": "residential", "hgv:conditional": "no @ (Mo-Fr 00:00-12:00;Sa 0:00-19:00); yes @ (Mo-Fr 12:00-24:00;Sa 19:00-24:00)"},
                  {"dog": "leashed", "bicycle": "dismount"},
                 ]:
            assert not a.way(None, t, None), a.way(None, t, None)
            assert not a.node(None, t), a.node(None, t)

        # Valid ways with directions or lanes
        for t in [{"highway": "residential", "vehicle:forward": "customers"},
                  {"highway": "residential", "vehicle:backward:conditional": "customers @ (wet); destination @ (snow)"},
                  {"highway": "residential", "vehicle:both_ways": "customers;destination"},
                  {"highway": "residential", "vehicle:both_ways": "customers; destination"},
                  {"highway": "residential", "bicycle:forward:conditional": "dismount@wet"},
                  {"highway": "residential", "bicycle:forward:lanes": "no|designated|||yes|none||variable|dismount"},
                  {"highway": "residential", "bicycle:lanes:conditional": "no|designated|yes @ Su"},
                  {"highway": "residential", "bicycle:lanes:forward:conditional": "none||variable|yes @ (Su;Sa); no|no|yes @ snow"},
                 ]:
            assert not a.way(None, t, None), a.way(None, t, None)

        # Invalid nodes and ways
        for t in [{"amenity": "parking", "vehicle": "nope"},
                  {"amenity": "parking", "vehicle": "none"},
                  {"amenity": "parking", "vehicle:conditional": "nope @ wet"},
                  {"highway": "residential", "canoe:conditional": "no @ (Mo-Fr 06:00-11:00;Sa 03:30-19:00); nope @ (snow)"},
                  {"highway": "residential", "tank:conditional": "dismount @ (Mo-Fr 06:00-11:00;Sa 03:30-19:00); no @ (snow)"},
                  {"bicycle": "leashed"},
                 ]:
            self.check_err(a.way(None, t, None), expected = {'class': 30404})
            self.check_err(a.node(None, t), expected = {'class': 30404})

        # Invalid ways with directions or lanes
        for t in [{"highway": "residential", "vehicle:forward": "nope"},
                  {"highway": "residential", "vehicle:both_ways:conditional": "nope @ wet"},
                  {"highway": "residential", "horse:backward": "customers;nope"},
                  {"highway": "residential", "horse:backward": "nope; customers"},
                  {"highway": "residential", "horse:lanes": "yes|nope|yes|nope|"},
                  {"highway": "residential", "snowmobile:lanes:backward:conditional": "nope|yes @ wet; yes|yes @ snow"},
                  {"highway": "residential", "hgv:lanes": "no @ (weight>7.5)|yes|yes"},
                 ]:
            self.check_err(a.way(None, t, None), expected = {'class': 30404})

        # Transport mode as tag value
        for t in [{"highway": "residential", "access": "foot"},
                  {"highway": "residential", "access:conditional": "foot @ yes"},
                  {"highway": "residential", "access:forward": "bus;foot"},
                  {"highway": "residential", "access": "bus; destination"},
                  {"highway": "residential", "access": "emergency"},
                  {"highway": "residential", "access:lanes": "bus|agricultural|yes"},
                  {"highway": "residential", "access:lanes:forward:conditional": "bus|agricultural|yes @ snow"},
                 ]:
            self.check_err(a.way(None, t, None), expected = {'class': 30405})
