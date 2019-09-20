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
from typing import Optional, Callable, Dict, Union

from lxml import etree

from swim_aim.data_mappers.xml import MappedValueType

__author__ = "EUROCONTROL (SWIM)"


class MapperField:

    def __init__(self,
                 xpath: str,
                 post_map: Optional[Callable] = None,
                 namespaces: Optional[Dict[str, str]] = None,
                 strict: Optional[bool] = True) -> None:
        """
        :param xpath: the xpath of the element that this field represents (maps)
        :param post_map: a callable to be called the respective element has been mapped
        :param namespaces: the namespaces used in the XML file where the element comes from
        :param strict: to be used for strict validation of the mapped value
        """
        if not xpath.startswith('./'):
            raise ValueError('Invalid xpath')

        self.xpath = xpath
        self.namespaces = namespaces
        self.strict = strict
        self._post_map = post_map
        self._xpath_tree = xpath.split('/')
        self._xpath_leaf = self._xpath_tree[-1]

    def _get_value_from_element(self, element: etree.Element) -> MappedValueType:
        """
        Retrieves the value of the provided element based on the xpath

        :param element:
        :return:
        """
        # the xpath is deeper than one element
        if len(self._xpath_tree) > 1:
            element = element.find(self.xpath, self.namespaces)

        return element.text if element is not None else None

    def _get_value_from_attribute(self, element: etree.Element) -> MappedValueType:
        """
        Retrieves the value of the attribute specified in the xpath from the provided element

        :param element:
        :return:
        """
        # discard @ from the beginning of the attribute name
        attribute_name = self._xpath_leaf[1:]

        # cleanup attribute_name in case it contains namespace code .i.e xlink:href
        if ':' in attribute_name:
            ns_code, attr_name = attribute_name.split(':')
            namespace = self.namespaces[ns_code]
            attribute_name = f'{{{namespace}}}{attr_name}'

        # the xpath is deeper than one element (plus the attribute name)
        if len(self._xpath_tree) > 2:
            xpath_path = "/".join(self._xpath_tree[:-1])
            element = element.find(xpath_path, self.namespaces)

        return element.get(attribute_name) if element is not None else None

    def _get_value(self, element):
        func = self._get_value_from_attribute if self._xpath_leaf.startswith('@') else self._get_value_from_element

        return func(element)

    def from_xml(self, element: etree.Element) -> MappedValueType:
        """
        The main function to be called in order to retrieve the value of an XML element or attribute
        :param element:
        :return:
        """
        value = self._get_value(element)

        if self._post_map and value is not None:
            value = self._post_map(value)

        return value


class IntegerMapperField(MapperField):

    def _get_value(self, element: etree.Element) -> Union[int, str, None]:
        """
        Overrides the parent method by converting the XML value to integer.
        :param element:
        :return:
        """
        value: str = super()._get_value(element)

        try:
            return int(value)
        except (ValueError, TypeError):
            if self.strict:
                raise

            return value


class FloatMapperField(MapperField):

    def _get_value(self, element: etree.Element) -> Union[float, str, None]:
        """
        Overrides the parent method by converting the XML value to float.

        :param element:
        :return:
        """
        value: str = super()._get_value(element)

        try:
            return float(value)
        except (ValueError, TypeError):
            if self.strict:
                raise

            return value


class DatetimeMapperField(MapperField):

    def __init__(self, xpath: str, str_format: str = '%Y-%m-%dT%H:%M:%S', **kwargs) -> None:
        """

        :param xpath:
        :param str_format:
        :param kwargs:
        """
        super().__init__(xpath, **kwargs)
        self.str_format = str_format

    def _get_value(self, element: etree.Element) -> Union[datetime, None]:
        """
        Overrides the parent method by converting the XML value to datetime.

        :param element:
        :return:
        """
        value: str = super()._get_value(element)

        return datetime.strptime(value, self.str_format) if value else None
