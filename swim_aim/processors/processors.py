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
from swim_aim.processors import DataProcessor, DataProcessorContext
from swim_aim.xml.mapper import xml_map

__author__ = "EUROCONTROL (SWIM)"


class XMLMapProcessor(DataProcessor):

    def process(self, context: DataProcessorContext) -> None:
        print(f"Mapping XML file: {context.file}")
        xml_mappers = xml_map(file_path=context.file,
                              mapper_class=context.xml_mapper_class)

        context.xml_mappers = xml_mappers


class DbMapProcessor(DataProcessor):

    def process(self, context: DataProcessorContext) -> None:
        db_objects = []
        for xml_mapper in context.xml_mappers:
            print(f"Mapping XML to DB object: {xml_mapper.__class__}")
            db_objects.append(context.db_mapper(xml_mapper))

        context.db_objects = db_objects


class DbSaveProcessor(DataProcessor):

    def process(self, context: DataProcessorContext) -> None:
        for db_object in context.db_objects:
            print(f"Saving db object: {db_object}")
            context.db_saver(db_object)
