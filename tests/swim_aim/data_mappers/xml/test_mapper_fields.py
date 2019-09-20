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
from datetime import datetime
from unittest import mock

import pytest
from lxml import etree

from swim_aim.data_mappers.xml import NAMESPACES
from swim_aim.data_mappers.xml.mapper_fields import XMLMapperField, DatetimeXMLMapperField, FloatXMLMapperField, \
    IntegerXMLMapperField

__author__ = "EUROCONTROL (SWIM)"


@pytest.mark.parametrize('xpath', [
    '', 'invalid_xpath', 'invalid xpath', 'invalid.xpath', 'invalid:xpath'
])
def test_mapper_field__xpath_not_separated_by_slashes__raises_valueerror(xpath):
    with pytest.raises(ValueError) as e:
        XMLMapperField(xpath)
        assert 'Invalid xpath' == str(e.value)


@mock.patch.object(XMLMapperField, '_get_value', return_value=None)
def test_integer_mapper_field__invalid_value__raises_on_strict_mode(mock_mapper_field):
    imf = IntegerXMLMapperField('./some/xpath', strict=True)

    with pytest.raises(TypeError) as e:
        imf.from_xml(mock.Mock())


@mock.patch.object(XMLMapperField, '_get_value', return_value='some_value')
def test_integer_mapper_field__returns_value_on_strict_mode_false(mock_mapper_field):
    imf = IntegerXMLMapperField('./some/xpath', strict=False)

    assert 'some_value' == imf.from_xml(mock.Mock())


@mock.patch.object(XMLMapperField, '_get_value', return_value=None)
def test_float_mapper_field__invalid_value__raises_on_strict_mode(mock_mapper_field):
    fmf = FloatXMLMapperField('./some/xpath', strict=True)

    with pytest.raises(TypeError) as e:
        fmf.from_xml(mock.Mock())


@mock.patch.object(XMLMapperField, '_get_value', return_value='some_value')
def test_float_mapper_field__returns_value_on_strict_mode_false(mock_mapper_field):
    imf = FloatXMLMapperField('./some/xpath', strict=False)

    assert 'some_value' == imf.from_xml(mock.Mock())


@mock.patch.object(XMLMapperField, '_get_value', return_value=None)
def test_datetime_mapper_field__mapped_value_is_none__returns_none(mock_mapper_field):
    dmf = DatetimeXMLMapperField('./some/xpath', strict=True)

    assert dmf.from_xml(mock.Mock()) is None


@pytest.mark.parametrize('xml_string, xpath, mapper_field_class, expected_mapped_value', [
    (
        # string from element
        """<?xml version='1.0' encoding='UTF-8'?><adrmsg:ADRMessage xmlns:adrmsg="http://www.eurocontrol.int/cfmu/b2b/ADRMessage" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="ID_5052_1548813652630_1">
            <adrmsg:hasMember>
            <aixm:AirportHeliport xmlns:aixm="http://www.aixm.aero/schema/5.1" gml:id="ID_5052_1548813652630_2">
                <gml:identifier codeSpace="urn:uuid:">2193b095-8bd7-40e4-ba10-2a5a3cf29901</gml:identifier>
            </aixm:AirportHeliport>
            </adrmsg:hasMember>
        </adrmsg:ADRMessage>
        """.encode('utf-8'),
        './gml:identifier',
        XMLMapperField,
        '2193b095-8bd7-40e4-ba10-2a5a3cf29901'
    ),
    (
        # datetime from element
        """<?xml version='1.0' encoding='UTF-8'?><adrmsg:ADRMessage xmlns:adrmsg="http://www.eurocontrol.int/cfmu/b2b/ADRMessage" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="ID_5052_1548813652630_1">
            <adrmsg:hasMember>
            <aixm:AirportHeliport xmlns:aixm="http://www.aixm.aero/schema/5.1" gml:id="ID_5052_1548813652630_2">
            <aixm:timeSlice>
                <aixm:AirportHeliportTimeSlice gml:id="ID_5052_1548813652630_3">
                    <aixm:featureLifetime>
                        <gml:TimePeriod gml:id="ID_5052_1548813652630_5">
                            <gml:beginPosition>2013-11-14T00:00:00</gml:beginPosition>
                            <gml:endPosition indeterminatePosition="unknown"/>
                        </gml:TimePeriod>
                    </aixm:featureLifetime>
                </aixm:AirportHeliportTimeSlice>
            </aixm:timeSlice>
            </aixm:AirportHeliport>
            </adrmsg:hasMember>
        </adrmsg:ADRMessage>
        """.encode('utf-8'),
        './aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:beginPosition',
        DatetimeXMLMapperField,
        datetime(2013, 11, 14, 0, 0, 0)
    ),
    (
        # float from element
        """<?xml version='1.0' encoding='UTF-8'?><adrmsg:ADRMessage xmlns:adrmsg="http://www.eurocontrol.int/cfmu/b2b/ADRMessage" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="ID_5052_1548813652630_1">
            <adrmsg:hasMember>
            <aixm:AirportHeliport xmlns:aixm="http://www.aixm.aero/schema/5.1" gml:id="ID_5052_1548813652630_2">
            <aixm:timeSlice>
                <aixm:AirportHeliportTimeSlice gml:id="ID_5052_1548813652630_3">
                    <aixm:ARP>
                        <aixm:ElevatedPoint gml:id="ID_5052_1548813652630_7">
                            <gml:pos srsName="urn:ogc:def:crs:EPSG::4326">-8.698333333333334 160.67833333333334</gml:pos>
                            <aixm:elevation uom="FT">100.5</aixm:elevation>
                        </aixm:ElevatedPoint>
                    </aixm:ARP>
                </aixm:AirportHeliportTimeSlice>
            </aixm:timeSlice>
            </aixm:AirportHeliport>
            </adrmsg:hasMember>
        </adrmsg:ADRMessage>
        """.encode('utf-8'),
        './aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:ARP/aixm:ElevatedPoint/aixm:elevation',
        FloatXMLMapperField,
        100.5
    ),
    (
        # integer from element
        """<?xml version='1.0' encoding='UTF-8'?><adrmsg:ADRMessage xmlns:adrmsg="http://www.eurocontrol.int/cfmu/b2b/ADRMessage" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="ID_5052_1548813652630_1">
            <adrmsg:hasMember>
            <aixm:AirportHeliport xmlns:aixm="http://www.aixm.aero/schema/5.1" gml:id="ID_5052_1548813652630_2">
            <aixm:timeSlice>
                <aixm:AirportHeliportTimeSlice gml:id="ID_5052_1548813652630_3">
                    <aixm:ARP>
                        <aixm:ElevatedPoint gml:id="ID_5052_1548813652630_7">
                            <gml:pos srsName="urn:ogc:def:crs:EPSG::4326">-8.698333333333334 160.67833333333334</gml:pos>
                            <aixm:elevation uom="FT">100</aixm:elevation>
                        </aixm:ElevatedPoint>
                    </aixm:ARP>
                </aixm:AirportHeliportTimeSlice>
            </aixm:timeSlice>
            </aixm:AirportHeliport>
            </adrmsg:hasMember>
        </adrmsg:ADRMessage>
        """.encode('utf-8'),
        './aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:ARP/aixm:ElevatedPoint/aixm:elevation',
        IntegerXMLMapperField,
        100
    ),
    (
        # string from attribute
        """<?xml version='1.0' encoding='UTF-8'?><adrmsg:ADRMessage xmlns:adrmsg="http://www.eurocontrol.int/cfmu/b2b/ADRMessage" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="ID_5052_1548813652630_1">
            <adrmsg:hasMember>
            <aixm:AirportHeliport xmlns:aixm="http://www.aixm.aero/schema/5.1" gml:id="ID_5052_1548813652630_2">
            <aixm:timeSlice>
                <aixm:AirportHeliportTimeSlice gml:id="ID_5052_1548813652630_3">
                    <aixm:ARP>
                        <aixm:ElevatedPoint gml:id="ID_5052_1548813652630_7">
                            <gml:pos srsName="urn:ogc:def:crs:EPSG::4326">-8.698333333333334 160.67833333333334</gml:pos>
                            <aixm:elevation uom="FT">100.5</aixm:elevation>
                        </aixm:ElevatedPoint>
                    </aixm:ARP>
                </aixm:AirportHeliportTimeSlice>
            </aixm:timeSlice>
            </aixm:AirportHeliport>
            </adrmsg:hasMember>
        </adrmsg:ADRMessage>
        """.encode('utf-8'),
        './aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:ARP/aixm:ElevatedPoint/aixm:elevation/@uom',
        XMLMapperField,
        'FT'
    )
])
def test_mapper_field__from_xml_returns_the_correct_value(xml_string, xpath, mapper_field_class, expected_mapped_value):
    xml = etree.fromstring(xml_string)
    element = xml.find('./adrmsg:hasMember/aixm:AirportHeliport', NAMESPACES)

    mf = mapper_field_class(xpath=xpath, namespaces=NAMESPACES)

    assert expected_mapped_value == mf.from_xml(element)


@pytest.mark.parametrize('xml_string, xpath, mapper_field_class, expected_mapped_value', [
    (
        # string from attribute with namespace
        """<?xml version='1.0' encoding='UTF-8'?><adrmsg:ADRMessage xmlns:adrmsg="http://www.eurocontrol.int/cfmu/b2b/ADRMessage" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="ID_5052_1548813652630_1">
                <adrmsg:hasMember>
                <aixm:RouteSegment xmlns:aixm="http://www.aixm.aero/schema/5.1" gml:id="ID_5063_1548813656537_2">
                    <gml:identifier codeSpace="urn:uuid:">5f7c0b50-b667-470e-953f-8ae479a5df3e</gml:identifier>
                    <aixm:timeSlice>
                        <aixm:RouteSegmentTimeSlice gml:id="ID_5063_1548813656537_3">
                            <aixm:start>
                                <aixm:EnRouteSegmentPoint gml:id="ID_5063_1548813656537_6">
                                    <aixm:pointChoice_navaidSystem xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                   xlink:href="urn:uuid:ed74d8c5-91c6-4567-a95d-602cd48c19f4"/>
                                </aixm:EnRouteSegmentPoint>
                            </aixm:start>
                        </aixm:RouteSegmentTimeSlice>
                    </aixm:timeSlice>
                </aixm:RouteSegment>
                </adrmsg:hasMember>
            </adrmsg:ADRMessage>
        """.encode('utf-8'),
        './aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:start/aixm:EnRouteSegmentPoint/*[@xlink:href]/@xlink:href',
        XMLMapperField,
        'urn:uuid:ed74d8c5-91c6-4567-a95d-602cd48c19f4'
    )
])
def test_mapper_field__maps_attribute_with_namespace(xml_string, xpath, mapper_field_class, expected_mapped_value):
    xml = etree.fromstring(xml_string)
    element = xml.find('./adrmsg:hasMember/aixm:RouteSegment', NAMESPACES)

    mf = mapper_field_class(xpath=xpath, namespaces=NAMESPACES)

    assert expected_mapped_value == mf.from_xml(element)

@pytest.mark.parametrize('xml_string, xpath, mapper_field_class, expected_mapped_value', [
    (
        # string from attribute with namespace
        """<?xml version='1.0' encoding='UTF-8'?><adrmsg:ADRMessage xmlns:adrmsg="http://www.eurocontrol.int/cfmu/b2b/ADRMessage" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="ID_5052_1548813652630_1">
                <adrmsg:hasMember>
                <aixm:RouteSegment xmlns:aixm="http://www.aixm.aero/schema/5.1" gml:id="ID_5063_1548813656537_2">
                    <gml:identifier codeSpace="urn:uuid:">5f7c0b50-b667-470e-953f-8ae479a5df3e</gml:identifier>
                    <aixm:timeSlice>
                        <aixm:RouteSegmentTimeSlice gml:id="ID_5063_1548813656537_3">
                            <aixm:start>
                                <aixm:EnRouteSegmentPoint gml:id="ID_5063_1548813656537_6">
                                    <aixm:pointChoice_navaidSystem xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                   xlink:href="urn:uuid:ed74d8c5-91c6-4567-a95d-602cd48c19f4"/>
                                </aixm:EnRouteSegmentPoint>
                            </aixm:start>
                        </aixm:RouteSegmentTimeSlice>
                    </aixm:timeSlice>
                </aixm:RouteSegment>
                </adrmsg:hasMember>
            </adrmsg:ADRMessage>
        """.encode('utf-8'),
        './aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:start/aixm:EnRouteSegmentPoint/*[@xlink:href]/@xlink:href',
        XMLMapperField,
        'ed74d8c5-91c6-4567-a95d-602cd48c19f4'
    )
])
def test_mapper_field__maps_attribute_with_namespace_with_post_map(xml_string, xpath, mapper_field_class,
                                                                   expected_mapped_value):
    xml = etree.fromstring(xml_string)
    element = xml.find('./adrmsg:hasMember/aixm:RouteSegment', NAMESPACES)

    mf = mapper_field_class(xpath=xpath, namespaces=NAMESPACES, post_map=lambda v: v.replace('urn:uuid:', ''))

    assert expected_mapped_value == mf.from_xml(element)

