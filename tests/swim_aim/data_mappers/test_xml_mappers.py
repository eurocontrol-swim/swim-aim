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
import os

import pytest

from swim_xml.mapper import xml_map
from swim_aim.data_mappers.xml_mappers import AirportHeliportXMLMapper, DesignatedPointXMLMapper, NavaidXMLMapper, \
    RouteSegmentXMLMapper, remove_urn_uuid
from tests import TEST_DIR

__author__ = "EUROCONTROL (SWIM)"


@pytest.mark.parametrize('string, expected_string', [
    ('urn:uuid:024bb6f8-3265-472a-9988-c765f519bcef', '024bb6f8-3265-472a-9988-c765f519bcef'),
    ('024bb6f8-3265-472a-9988-c765f519bcef', '024bb6f8-3265-472a-9988-c765f519bcef')
])
def test_remove_urn_uuid(string, expected_string):
    assert expected_string == remove_urn_uuid(string)


@pytest.mark.parametrize('xml_path, mapper_class, expected_mapper', [
    (
        'static/AirportHeliport.xml',
        AirportHeliportXMLMapper,
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
        )
    ),
    (
        'static/DesignatedPoint.xml',
        DesignatedPointXMLMapper,
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
        )
    ),
    (
        'static/Navaid.xml',
        NavaidXMLMapper,
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
        )
    ),
    (
        'static/Route.xml',
        RouteXMLMapper,
        RouteXMLMapper(
            identifier='024bb6f8-3265-472a-9988-c765f519bcef',
            interpretation='BASELINE',
            designator_prefix=None,
            designator_second_letter='A',
            designator_number=100,
            type='ATS',
            begin_lifetime=None,
            end_lifetime=None
        )
    ),
    (
        'static/RouteSegment.xml',
        RouteSegmentXMLMapper,
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
        )
    )
])
def test_mapper(xml_path, mapper_class, expected_mapper):
    xml_path = os.path.join(TEST_DIR, xml_path)

    assert [expected_mapper] == xml_map(xml_path, mapper_class)


@pytest.mark.parametrize('mapper, expected_dict', [
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
        {
            'identifier': '2193b095-8bd7-40e4-ba10-2a5a3cf29901',
            'interpretation': 'BASELINE',
            'name': "AUKI/GWAUNARU'U",
            'icao_location_indicator': 'AGGA',
            'iata_designator': 'AKS',
            'type': 'OTHER',
            'control_type': 'CIVIL',
            'position': '-8.698333333333334 160.67833333333334',
            'srs_name': 'urn:ogc:def:crs:EPSG::4326',
            'elevation': 0.0,
            'elevation_uom': 'FT',
            'begin_lifetime': datetime.datetime(2013, 11, 14, 0, 0),
            'end_lifetime': None,
        }
    ),
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
        {
            'identifier': '2e71b1e5-735e-4f46-b986-52271dc22c7d',
            'interpretation': 'BASELINE',
            'name': '10N030W',
            'designator': None,
            'type': 'COORD',
            'position': '10.0 -30.0',
            'srs_name': 'urn:ogc:def:crs:EPSG::4326',
            'elevation': None,
            'elevation_uom': None,
            'begin_lifetime': datetime.datetime(2006, 6, 8, 0, 0),
            'end_lifetime': None
        }
    ),
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
        {
            'identifier': '9f9a0a70-cacb-4435-81b8-f99348371a9f',
            'interpretation': 'BASELINE',
            'name': 'AASIAAT',
            'designator': 'AA',
            'type': 'NDB_MKR',
            'position': '68.72305555555556 -52.78472222222222',
            'srs_name': 'urn:ogc:def:crs:EPSG::4326',
            'elevation': None,
            'elevation_uom': None,
            'begin_lifetime': datetime.datetime(2010, 4, 8, 0, 0),
            'end_lifetime': None,
        }
    ),
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
        {
            'identifier': '024bb6f8-3265-472a-9988-c765f519bcef',
            'interpretation': 'BASELINE',
            'designator_prefix': None,
            'designator_second_letter': 'A',
            'designator_number': 100,
            'type': 'ATS',
            'begin_lifetime': None,
            'end_lifetime': None
        }
    ),
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
        {
            'identifier': '5f7c0b50-b667-470e-953f-8ae479a5df3e',
            'interpretation': 'BASELINE',
            'start': 'ed74d8c5-91c6-4567-a95d-602cd48c19f4',
            'end': 'c80de58f-5a48-4308-9239-cf699429b4b0',
            'upper_limit': 430,
            'upper_limit_uom': 'FL',
            'upper_limit_ref': 'STD',
            'lower_limit': 265,
            'lower_limit_uom': 'FL',
            'lower_limit_ref': 'STD',
            'route_formed': '024bb6f8-3265-472a-9988-c765f519bcef',
            'begin_lifetime': datetime.datetime(2018, 3, 29, 0, 0),
            'end_lifetime': None
        }
    )
])
def test_mapper__to_dict(mapper, expected_dict):
    assert expected_dict == mapper.to_dict()

