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
from swim_aim.xml.mapper import Mapper
from swim_aim.xml.mapper_fields import MapperField, FloatMapperField, DatetimeMapperField, IntegerMapperField

__author__ = "EUROCONTROL (SWIM)"


def remove_urn_uuid(value):
    return value.replace('urn:uuid:', '')


class AirportHeliportMapper(Mapper):

    root_xpath = './adrmsg:hasMember/aixm:AirportHeliport'

    identifier = MapperField(xpath='./gml:identifier', post_map=remove_urn_uuid)
    interpretation = MapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:interpretation')
    name = MapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:name')
    icao_location_indicator = MapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:locationIndicatorICAO')
    iata_designator = MapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:designatorIATA')
    type = MapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:type')
    control_type = MapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:controlType')
    position = MapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:ARP/aixm:ElevatedPoint/gml:pos')
    srs_name = MapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:ARP/aixm:ElevatedPoint/gml:pos/@srsName')
    elevation = FloatMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:ARP/aixm:ElevatedPoint/aixm:elevation')
    elevation_uom = MapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:ARP/aixm:ElevatedPoint/aixm:elevation/@uom')
    begin_lifetime = DatetimeMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:beginPosition')
    end_lifetime = DatetimeMapperField(xpath='./aixm:timeSlice/aixm:AirportHeliportTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:endPosition')


class NavaidMapper(Mapper):

    root_xpath = './adrmsg:hasMember/aixm:Navaid'

    identifier = MapperField(xpath='./gml:identifier', post_map=remove_urn_uuid)
    interpretation = MapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:interpretation')
    name = MapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:name')
    designator = MapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:designator')
    type = MapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:type')
    position = MapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:location/aixm:ElevatedPoint/gml:pos')
    srs_name = MapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:location/aixm:ElevatedPoint/gml:pos/@srsName')
    elevation = FloatMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:location/aixm:ElevatedPoint/aixm:elevation',
                                 strict=False)
    elevation_uom = MapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:location/aixm:ElevatedPoint/aixm:elevation/@uom')
    begin_lifetime = DatetimeMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:beginPosition')
    end_lifetime = DatetimeMapperField(xpath='./aixm:timeSlice/aixm:NavaidTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:endPosition')


class DesignatedPointMapper(Mapper):

    root_xpath = './adrmsg:hasMember/aixm:DesignatedPoint'

    identifier = MapperField(xpath='./gml:identifier', post_map=remove_urn_uuid)
    interpretation = MapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:interpretation')
    name = MapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:name')
    designator = MapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:designator')
    type = MapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:type')
    position = MapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:location/aixm:Point/gml:pos')
    srs_name = MapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:location/aixm:Point/gml:pos/@srsName')
    elevation = FloatMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:location/aixm:Point/aixm:elevation',
                                 strict=False)
    elevation_uom = MapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:location/aixm:Point/aixm:elevation/@uom')
    begin_lifetime = DatetimeMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:beginPosition')
    end_lifetime = DatetimeMapperField(xpath='./aixm:timeSlice/aixm:DesignatedPointTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:endPosition')


class RouteMapper(Mapper):

    root_xpath = './adrmsg:hasMember/aixm:Route'

    identifier = MapperField(xpath='./gml:identifier')
    interpretation = MapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:interpretation')
    designator_prefix = MapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:designatorPrefix')
    designator_second_letter = MapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:designatorSecondLetter')
    designator_number = IntegerMapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:designatorNumber',
                                           strict=False)
    type = MapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:type')
    begin_lifetime = DatetimeMapperField(xpath='./aixm:timeSlice/aixm:RoutetTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:beginPosition')
    end_lifetime = DatetimeMapperField(xpath='./aixm:timeSlice/aixm:RouteTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:endPosition')


class RouteSegmentMapper(Mapper):

    root_xpath = './adrmsg:hasMember/aixm:RouteSegment'

    identifier = MapperField(xpath='./gml:identifier', post_map=remove_urn_uuid)
    interpretation = MapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:interpretation')
    start = MapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:start/aixm:EnRouteSegmentPoint/*[@xlink:href]/@xlink:href',
                        post_map=remove_urn_uuid)
    end = MapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:end/aixm:EnRouteSegmentPoint/*[@xlink:href]/@xlink:href',
                      post_map=remove_urn_uuid)
    upper_limit = IntegerMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:upperLimit', strict=False)
    upper_limit_uom = MapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:upperLimit/@uom')
    upper_limit_ref = MapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:upperLimitReference')
    lower_limit = IntegerMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:lowerLimit', strict=False)
    lower_limit_uom = MapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:lowerLimit/@uom')
    lower_limit_ref = MapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:lowerLimitReference')
    route_formed = MapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:routeFormed/@xlink:href',
                               post_map=remove_urn_uuid)
    begin_lifetime = DatetimeMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:beginPosition')
    end_lifetime = DatetimeMapperField(xpath='./aixm:timeSlice/aixm:RouteSegmentTimeSlice/aixm:featureLifetime/gml:TimePeriod/gml:endPosition')

