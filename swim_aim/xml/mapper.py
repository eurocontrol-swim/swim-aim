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
from typing import List, Type, Dict

from lxml import etree

from swim_aim.xml import MappedValueType, NAMESPACES
from swim_aim.xml.mapper_fields import XMLMapperField

__author__ = "EUROCONTROL (SWIM)"


class MetaMapper(type):

    def __new__(mcs, name, bases, attrs):
        """
        Makes checks on classes' definitions and updates the defined XMLMapperField attributes of the class

        :param name: the name of the class to be created
        :param bases: the classes to inherit from
        :param attrs: the defined class attributes
        :return: XMLMapper class
        """
        if name != 'XMLMapper':
            if 'root_xpath' not in attrs.keys():
                raise ValueError(f'root_xpath is missing from {name} class definition')

            # supply all the classes that inherit from XMLMapper with the namespaces
            mapper_fields = {}
            for attr_name, attr in attrs.items():
                if isinstance(attr, XMLMapperField):
                    attr.namespaces = NAMESPACES
                    mapper_fields[attr_name] = attr
            attrs['mapper_fields'] = mapper_fields

        return type.__new__(mcs, name, bases, attrs)


class XMLMapper(metaclass=MetaMapper):

    root_xpath = ''

    def __init__(self, **kwargs):
        """
        When a mapper is simply instantiated all the defined XMLMapperField attributes are initialized as None because they
        are not mapped to any value yet, unless a value is provided via the constructor.
        """
        for attr, value in self.mapper_fields.items():
            if isinstance(value, XMLMapperField):
                self.__dict__[attr] = kwargs.get(attr)

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and other.__dict__ == self.__dict__

    def __ne__(self, other) -> bool:
        return not other == self

    @classmethod
    def from_xml(cls, element: etree.Element, instance=None):
        """
        Map the provided XML element to the XMLMapperField attributes of the class and returns a XMLMapper instance

        :param element: etree.Element
        :param instance: an existing XMLMapper instance can also be used to remap its XMLMapperField attributes
        :return: XMLMapper
        """
        instance = instance or cls()

        for mapper_field_name, mapper_field in cls.mapper_fields.items():
            mapped_value = mapper_field.from_xml(element)
            setattr(instance, mapper_field_name, mapped_value)
        return instance

    def to_dict(self) -> Dict[str, MappedValueType]:
        return {key: value for key, value in self.__dict__.items()
                if key in self.mapper_fields}


def xml_map(file_path: str, mapper_class: Type[XMLMapper]) -> List[Type[XMLMapper]]:
    """
    Parses a XML file and maps its element(s) to XMLMapper instance(s)

    :param file_path: the path of the XML file
    :param mapper_class:
    :return:
    """
    xml = etree.parse(file_path)

    elements = xml.findall(mapper_class.root_xpath, NAMESPACES)

    mappers = [mapper_class.from_xml(element) for element in elements]

    return mappers
