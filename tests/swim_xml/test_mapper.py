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
from unittest import mock

import pytest

from swim_xml.mapper import XMLMapper, xml_map
from swim_xml.mapper_fields import XMLMapperField
from swim_aim.data_mappers.xml_mappers import AirportHeliportXMLMapper
from tests import TEST_DIR

__author__ = "EUROCONTROL (SWIM)"


def test_mapper_class_definition__root_xpath_is_missing__raises_value_error():
    with pytest.raises(ValueError) as e:
        class MyXMLMapper(XMLMapper):
            pass
        assert f'root_xpath is missing from {MyXMLMapper.__name__} class definition' == str(e.value)


def test_mapper_class_instantiation__instance_has_all_the_mapper_fields_assigned_as_none():
    class MyXMLMapper(XMLMapper):
        root_xpath = 'path'

        field1 = XMLMapperField(xpath='./xpath')
        field2 = XMLMapperField(xpath='./xpath')
        field3 = XMLMapperField(xpath='./xpath')

    my_mapper = MyXMLMapper()
    assert my_mapper.field1 is None
    assert my_mapper.field2 is None
    assert my_mapper.field3 is None


@mock.patch.object(XMLMapperField, 'from_xml', return_value='value')
def test_mapper__map_returns_instance_with_mapped_values_on_the_mapped_fields(mock_from_xml):

    class MyXMLMapper(XMLMapper):
        root_xpath = 'path'

        field1 = XMLMapperField(xpath='./xpath')
        field2 = XMLMapperField(xpath='./xpath')
        field3 = XMLMapperField(xpath='./xpath')

    my_mapper = MyXMLMapper.map(mock.Mock())

    assert 'value' == my_mapper.field1
    assert 'value' == my_mapper.field2
    assert 'value' == my_mapper.field3


@mock.patch.object(XMLMapperField, 'from_xml', return_value='value')
def test_mapper__from_dict(mock_from_xml):

    class MyXMLMapper(XMLMapper):
        root_xpath = 'path'

        field1 = XMLMapperField(xpath='./xpath')
        field2 = XMLMapperField(xpath='./xpath')
        field3 = XMLMapperField(xpath='./xpath')

    my_mapper = MyXMLMapper.map(mock.Mock())

    assert {
        'field1': 'value',
        'field2': 'value',
        'field3': 'value'
    } == my_mapper.to_dict()


def test_xml_map__returns_list_of_mapper_instances_of_the_provided_class():
    xml_path = os.path.join(TEST_DIR, 'static/AirportHeliport.xml')
    mappers = xml_map(xml_path, AirportHeliportXMLMapper)

    assert isinstance(mappers, list)
    assert all([isinstance(mapper, AirportHeliportXMLMapper) for mapper in mappers])
