"""
Copyright 2019 EUROCONTROL
==========================================

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the 
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following 
   disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following 
   disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products 
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE 
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

==========================================

Editorial note: this license is an instance of the BSD license template as provided by the Open Source Initiative: 
http://opensource.org/licenses/BSD-3-Clause

Details on EUROCONTROL: http://www.eurocontrol.int
"""
from typing import Dict, Union

from swim_aim.data_mappers.xml import MappedValueType
from swim_aim.data_mappers.xml_mappers import AirportHeliportXMLMapper, DesignatedPointXMLMapper, NavaidXMLMapper, RouteXMLMapper, \
    RouteSegmentXMLMapper
from swim_aim.db.models import AirportHeliport, Point, Route, RouteSegment, POINT_TYPE
from swim_aim.provision.utils import string_to_coordinates

__author__ = "EUROCONTROL (SWIM)"


def handle_position(mapper_dict: Dict[str, MappedValueType]) -> Dict[str, MappedValueType]:
    mapper_dict['latitude'], mapper_dict['longitude'] = string_to_coordinates(mapper_dict['position'])

    del mapper_dict['position']

    return mapper_dict


def convert_to_airport_heliport(airport_heliport_mapper: AirportHeliportXMLMapper) -> AirportHeliport:
    airport_heliport_mapper_dict = airport_heliport_mapper.to_dict()

    airport_heliport_mapper_dict = handle_position(airport_heliport_mapper_dict)

    return AirportHeliport(**airport_heliport_mapper_dict)


def convert_to_point(point_mapper: Union[NavaidXMLMapper, DesignatedPointXMLMapper]) -> Point:
    point_mapper_dict = point_mapper.to_dict()

    point_mapper_dict = handle_position(point_mapper_dict)

    point_types = {
        NavaidXMLMapper: POINT_TYPE.NAVAID,
        DesignatedPointXMLMapper: POINT_TYPE.DESIGNATED_POINT
    }
    point_mapper_dict['point_type'] = point_types[point_mapper.__class__]

    return Point(**point_mapper_dict)


def convert_to_route(route_mapper: RouteXMLMapper) -> Route:
    return Route(**route_mapper.to_dict())


def convert_to_route_segment(route_segment_mapper: RouteSegmentXMLMapper) -> RouteSegment:
    return RouteSegment(**route_segment_mapper.to_dict())
