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

import pytest

from swim_aim.data_mappers.xml_mappers import AirportHeliportXMLMapper, NavaidXMLMapper, DesignatedPointXMLMapper, RouteXMLMapper, \
    RouteSegmentXMLMapper
from swim_aim.db.models import AirportHeliport, POINT_TYPE, Point, Route, RouteSegment
from swim_aim.provision.converters import convert_to_airport_heliport, convert_to_point, convert_to_route, \
    convert_to_route_segment

__author__ = "EUROCONTROL (SWIM)"


@pytest.mark.parametrize('mapper, expected_db_model', [
    (
        AirportHeliportXMLMapper(
            identifier='2193b095-8bd7-40e4-ba10-2a5a3cf29901',
            interpretation='BASELINE',
            name="AUKI/GWAUNARU'U",
            icao_location_indicator='AGGA',
            iata_designator='AKS',
            type='OTHER',
            control_type='CIVIL',
            position='-8.698333333333334 160.67833333333334',
            srs_name='urn:ogc:def:crs:EPSG::4326',
            elevation=0.0,
            elevation_uom='FT',
            begin_lifetime=datetime.datetime(2013, 11, 14, 0, 0),
            end_lifetime=None
        ),
        AirportHeliport(
            identifier='2193b095-8bd7-40e4-ba10-2a5a3cf29901',
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
    )
])
def test_convert_airport_heliport_mapper_to_airport_heliport_model(mapper, expected_db_model):
    assert expected_db_model == convert_to_airport_heliport(mapper)


@pytest.mark.parametrize('mapper, expected_db_model', [
    (
        NavaidXMLMapper(
            identifier='9f9a0a70-cacb-4435-81b8-f99348371a9f',
            interpretation='BASELINE',
            name='AASIAAT',
            designator='AA',
            type='NDB_MKR',
            position='68.72305555555556 -52.78472222222222',
            srs_name='urn:ogc:def:crs:EPSG::4326',
            elevation=None,
            elevation_uom=None,
            begin_lifetime=datetime.datetime(2010, 4, 8, 0, 0),
            end_lifetime=None
        ),
        Point(
            identifier='9f9a0a70-cacb-4435-81b8-f99348371a9f',
            interpretation='BASELINE',
            name='AASIAAT',
            designator='AA',
            type='NDB_MKR',
            latitude=68.72305555555556,
            longitude=-52.78472222222222,
            srs_name='urn:ogc:def:crs:EPSG::4326',
            elevation=None,
            elevation_uom=None,
            begin_lifetime=datetime.datetime(2010, 4, 8, 0, 0),
            end_lifetime=None,
            point_type=POINT_TYPE.NAVAID
        )
    )
])
def test_convert_navaid_mapper_to_point_model(mapper, expected_db_model):
    assert expected_db_model == convert_to_point(mapper)


@pytest.mark.parametrize('mapper, expected_db_model', [
    (
        DesignatedPointXMLMapper(
            identifier='2e71b1e5-735e-4f46-b986-52271dc22c7d',
            interpretation='BASELINE',
            name='10N030W',
            designator=None,
            type='COORD',
            position='10.0 -30.0',
            srs_name='urn:ogc:def:crs:EPSG::4326',
            elevation=None,
            elevation_uom=None,
            begin_lifetime=datetime.datetime(2006, 6, 8, 0, 0),
            end_lifetime=None
        ),
        Point(
            identifier='2e71b1e5-735e-4f46-b986-52271dc22c7d',
            interpretation='BASELINE',
            name='10N030W',
            designator=None,
            type='COORD',
            latitude=10.0,
            longitude=-30.0,
            srs_name='urn:ogc:def:crs:EPSG::4326',
            elevation=None,
            elevation_uom=None,
            begin_lifetime=datetime.datetime(2006, 6, 8, 0, 0),
            end_lifetime=None,
            point_type=POINT_TYPE.DESIGNATED_POINT
        )
    )
])
def test_convert_designated_point_mapper_to_point_model(mapper, expected_db_model):
    assert expected_db_model == convert_to_point(mapper)


@pytest.mark.parametrize('mapper, expected_db_model', [
    (
        RouteXMLMapper(
            identifier='024bb6f8-3265-472a-9988-c765f519bcef',
            interpretation='BASELINE',
            designator_prefix=None,
            designator_second_letter='A',
            designator_number=100,
            type='ATS',
            begin_lifetime=None,
            end_lifetime=None
        ),
        Route(
            identifier='024bb6f8-3265-472a-9988-c765f519bcef',
            interpretation='BASELINE',
            designator_prefix=None,
            designator_second_letter='A',
            designator_number=100,
            type='ATS',
            begin_lifetime=None,
            end_lifetime=None
        )
    )
])
def test_convert_route_mapper_to_route_model(mapper, expected_db_model):
    assert expected_db_model == convert_to_route(mapper)


@pytest.mark.parametrize('mapper, expected_db_model', [
    (
        RouteSegmentXMLMapper(
            identifier='5f7c0b50-b667-470e-953f-8ae479a5df3e',
            interpretation='BASELINE',
            start='ed74d8c5-91c6-4567-a95d-602cd48c19f4',
            end='c80de58f-5a48-4308-9239-cf699429b4b0',
            upper_limit=430,
            upper_limit_uom='FL',
            upper_limit_ref='STD',
            lower_limit=265,
            lower_limit_uom='FL',
            lower_limit_ref='STD',
            route_formed='024bb6f8-3265-472a-9988-c765f519bcef',
            begin_lifetime=datetime.datetime(2018, 3, 29, 0, 0),
            end_lifetime=None
        ),
        RouteSegment(
            identifier='5f7c0b50-b667-470e-953f-8ae479a5df3e',
            interpretation='BASELINE',
            start='ed74d8c5-91c6-4567-a95d-602cd48c19f4',
            end='c80de58f-5a48-4308-9239-cf699429b4b0',
            route_formed='024bb6f8-3265-472a-9988-c765f519bcef',
            upper_limit=430,
            upper_limit_uom='FL',
            upper_limit_ref='STD',
            lower_limit=265,
            lower_limit_uom='FL',
            lower_limit_ref='STD',
            begin_lifetime=datetime.datetime(2018, 3, 29, 0, 0),
            end_lifetime=None
        )
    )
])
def test_convert_route_segment_mapper_to_route_segment_model(mapper, expected_db_model):
    assert expected_db_model == convert_to_route_segment(mapper)

