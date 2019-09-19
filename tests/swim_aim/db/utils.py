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
import datetime
from uuid import uuid4

from swim_aim.db.models import AirportHeliport, Point, Route, RouteSegment

__author__ = "EUROCONTROL (SWIM)"


def unique_id():
    return uuid4().hex


def make_airport_heliport():
    return AirportHeliport(
        identifier=unique_id(),
        interpretation='BASELINE',
        name="AUKI/GWAUNARU'U",
        icao_location_indicator='AGGA',
        iata_designator='AKS',
        type='OTHER',
        control_type='CIVIL',
        latitude=-8.698333333333334,
        longitude=160.67833333333334,
        srs_name='urn:ogc:def:crs:EPSG::4326',
        elevation=0.0,
        elevation_uom='FT',
        begin_lifetime=datetime.datetime(2013, 11, 14, 0, 0),
        end_lifetime=None
    )


def make_point(point_type):
    return Point(
        identifier=unique_id(),
        interpretation='BASELINE',
        name='10N030W',
        designator='AA',
        type='COORD',
        latitude=10.0,
        longitude=-30.0,
        srs_name='urn:ogc:def:crs:EPSG::4326',
        elevation=None,
        elevation_uom=None,
        begin_lifetime=datetime.datetime(2006, 6, 8, 0, 0),
        end_lifetime=None,
        point_type=point_type
    )


def make_route():
    return Route(
        identifier=unique_id(),
        interpretation='BASELINE',
        designator_prefix=None,
        designator_second_letter='A',
        designator_number=100,
        type='ATS',
        begin_lifetime=None,
        end_lifetime=None
    )


def make_route_segment(point_type):
    return RouteSegment(
        identifier=unique_id(),
        interpretation='BASELINE',
        start_point=make_point(point_type),
        end_point=make_point(point_type),
        route=make_route(),
        upper_limit=430,
        upper_limit_uom='FL',
        upper_limit_ref='STD',
        lower_limit=265,
        lower_limit_uom='FL',
        lower_limit_ref='STD',
        begin_lifetime=datetime.datetime(2018, 3, 29, 0, 0),
        end_lifetime=None
    )
