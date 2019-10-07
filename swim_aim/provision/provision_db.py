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
import os

from swim_aim.data_mappers.db_mappers import map_from_airport_heliport_xml_mapper, map_from_point_xml_mapper, \
    map_from_route_xml_mapper, map_from_route_segment_xml_mapper
from swim_aim.data_mappers.xml_mappers import AirportHeliportXMLMapper, DesignatedPointXMLMapper, NavaidXMLMapper, \
    RouteXMLMapper, RouteSegmentXMLMapper
from swim_aim.db.airport_heliports import create_airport_heliport
from swim_aim.db.points import create_point
from swim_aim.network_manager.services.airspace_structure import AirspaceStructureService
from swim_aim.network_manager.services.file_download import NetworkManagerFileDownloadClient
from swim_aim.xml import xml_map

__author__ = "EUROCONTROL (SWIM)"


def save_airport_heliports(filename):
    xml_mappers = xml_map(filename, AirportHeliportXMLMapper)

    db_objects = [map_from_airport_heliport_xml_mapper(xml_mapper) for xml_mapper in xml_mappers]

    for db_object in db_objects:
        create_airport_heliport(db_object)


def save_designated_points(filename):
    xml_mappers = xml_map(filename, DesignatedPointXMLMapper)

    db_objects = [map_from_point_xml_mapper(xml_mapper) for xml_mapper in xml_mappers]

    for db_object in db_objects:
        create_point(db_object)


def save_navaids(filename):
    xml_mappers = xml_map(filename, NavaidXMLMapper)

    db_objects = [map_from_point_xml_mapper(xml_mapper) for xml_mapper in xml_mappers]

    for db_object in db_objects:
        create_point(db_object)


def save_routes(filename):
    xml_mappers = xml_map(filename, RouteXMLMapper)

    db_objects = [map_from_route_xml_mapper(xml_mapper) for xml_mapper in xml_mappers]

    for db_object in db_objects:
        create_point(db_object)


def save_route_segments(filename):
    xml_mappers = xml_map(filename, RouteSegmentXMLMapper)

    db_objects = [map_from_route_segment_xml_mapper(xml_mapper) for xml_mapper in xml_mappers]

    for db_object in db_objects:
        create_point(db_object)


def _get_basename(file_path):
    basename = os.path.basename(file_path)

    filename, _ = os.path.splitext(basename)

    return filename


FILE_HANDLERS = {
    'AirportHeliport': save_airport_heliports,
    'DesignatedPoint': save_designated_points,
    'Navaid': save_navaids,
    'Route': save_routes,
    'RouteSegment': save_route_segments
}


def main():
    cert = ('public', 'private')
    dest_folder = '/tmp'

    airspace_structure_service = AirspaceStructureService.create('wsdl_path', cert)

    download_client = NetworkManagerFileDownloadClient(cert)

    file_ids = airspace_structure_service.get_file_ids(user_id='tstxb2b7')

    all_files = [download_client.download(file_id, dest_folder) for file_id in file_ids]

    for filename in all_files:
        basename = _get_basename(filename)

        if basename in FILE_HANDLERS:
            FILE_HANDLERS[basename](filename)


if __name__ == '__main__':
    main()
