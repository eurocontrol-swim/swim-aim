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
from swim_xml.mapper import XMLMapper
from swim_xml.mapper_fields import XMLMapperField, FloatXMLMapperField, DatetimeXMLMapperField, IntegerXMLMapperField

__author__ = "EUROCONTROL (SWIM)"


def remove_urn_uuid(value: str) -> str:
    """
    Removes the leading 'urn:uuid:' from a string
    :param value:
    :return:
    """
    return value.replace('urn:uuid:', '')


class AirportHeliportXMLMapper(XMLMapper):

    root_xpath = './adrmsg:hasMember/aixm:AirportHeliport'

    identifier = XMLMapperField(xpath='./gml:identifier', post_map=remove_urn_uuid)
    interpretation = XMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:interpretation')
    name = XMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:name')
    icao_location_indicator = XMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:locationIndicatorICAO')
    iata_designator = XMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:designatorIATA')
    type = XMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:type')
    control_type = XMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:controlType')
    position = XMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:ARP/aixm:ElevatedPoint/gml:pos')
    srs_name = XMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:ARP/aixm:ElevatedPoint/gml:pos/@srsName')
    elevation = FloatXMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:ARP/aixm:ElevatedPoint/aixm:elevation')
    elevation_uom = XMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:ARP/aixm:ElevatedPoint/aixm:elevation/@uom')
    begin_lifetime = DatetimeXMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:beginPosition')
    end_lifetime = DatetimeXMLMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:endPosition')


class NavaidXMLMapper(XMLMapper):

    root_xpath = './adrmsg:hasMember/aixm:Navaid'

    identifier = XMLMapperField(xpath='./gml:identifier', post_map=remove_urn_uuid)
    interpretation = XMLMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:interpretation')
    name = XMLMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:name')
    designator = XMLMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:designator')
    type = XMLMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:type')
    position = XMLMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:location/aixm:ElevatedPoint/gml:pos')
    srs_name = XMLMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:location/aixm:ElevatedPoint/gml:pos/@srsName')
    elevation = FloatXMLMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:location/aixm:ElevatedPoint/aixm:elevation',
                                    strict=False)
    elevation_uom = XMLMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:location/aixm:ElevatedPoint/aixm:elevation/@uom')
    begin_lifetime = DatetimeXMLMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:beginPosition')
    end_lifetime = DatetimeXMLMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:endPosition')


class DesignatedPointXMLMapper(XMLMapper):

    root_xpath = './adrmsg:hasMember/aixm:DesignatedPoint'

    identifier = XMLMapperField(xpath='./gml:identifier', post_map=remove_urn_uuid)
    interpretation = XMLMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:interpretation')
    name = XMLMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:name')
    designator = XMLMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:designator')
    type = XMLMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:type')
    position = XMLMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:location/aixm:Point/gml:pos')
    srs_name = XMLMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:location/aixm:Point/gml:pos/@srsName')
    elevation = FloatXMLMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:location/aixm:Point/aixm:elevation',
                                    strict=False)
    elevation_uom = XMLMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:location/aixm:Point/aixm:elevation/@uom')
    begin_lifetime = DatetimeXMLMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:beginPosition')
    end_lifetime = DatetimeXMLMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:endPosition')


class RouteXMLMapper(XMLMapper):

    root_xpath = './adrmsg:hasMember/aixm:Route'

    identifier = XMLMapperField(xpath='./gml:identifier')
    interpretation = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:interpretation')
    designator_prefix = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:designatorPrefix')
    designator_second_letter = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:designatorSecondLetter')
    designator_number = IntegerXMLMapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:designatorNumber',
                                              strict=False)
    type = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:type')
    begin_lifetime = DatetimeXMLMapperField(xpath='./aixm:timeSlice/aixm:RoutetTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:beginPosition')
    end_lifetime = DatetimeXMLMapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:endPosition')


class RouteSegmentXMLMapper(XMLMapper):

    root_xpath = './adrmsg:hasMember/aixm:RouteSegment'

    identifier = XMLMapperField(xpath='./gml:identifier', post_map=remove_urn_uuid)
    interpretation = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:interpretation')
    start = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:start/aixm:EnRouteSegmentPoint/*[@xlink:href]/@xlink:href',
                           post_map=remove_urn_uuid)
    end = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:end/aixm:EnRouteSegmentPoint/*[@xlink:href]/@xlink:href',
                         post_map=remove_urn_uuid)
    upper_limit = IntegerXMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:upperLimit',
                                        strict=False)
    upper_limit_uom = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:upperLimit/@uom')
    upper_limit_ref = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:upperLimitReference')
    lower_limit = IntegerXMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:lowerLimit',
                                        strict=False)
    lower_limit_uom = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:lowerLimit/@uom')
    lower_limit_ref = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:lowerLimitReference')
    route_formed = XMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:routeFormed/@xlink:href',
                                  post_map=remove_urn_uuid)
    begin_lifetime = DatetimeXMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:beginPosition')
    end_lifetime = DatetimeXMLMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:endPosition')

