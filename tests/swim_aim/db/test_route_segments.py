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
import pytest

from swim_backend.db import db_save
from swim_aim.db.models import RouteSegment, POINT_TYPE
from swim_aim.db.route_segments import get_route_segment_by_id, get_route_segments, create_route_segment, \
    update_route_segment, delete_route_segment
from tests.swim_aim.db.utils import make_route_segment

__author__ = "EUROCONTROL (SWIM)"


@pytest.fixture
def generate_route_segment(session):
    def _generate_route_segment():
        route_segment = make_route_segment(POINT_TYPE.NAVAID)
        return db_save(session, route_segment)

    return _generate_route_segment


def test_get_route_segment_by_id__does_not_exist__returns_none():
    assert get_route_segment_by_id('1111') is None


def test_get_route_segment_by_id__object_exists_and_is_returned(generate_route_segment):
    route_segment = generate_route_segment()

    db_route_segment = get_route_segment_by_id(route_segment.identifier)

    assert isinstance(db_route_segment, RouteSegment)
    assert route_segment.identifier == db_route_segment.identifier


def test_get_route_segments__no_route_segment_in_db__returns_empty_list(generate_route_segment):
    db_route_segments = get_route_segments()

    assert [] == db_route_segments


def test_get_route_segments__existing_route_segments_are_returned(generate_route_segment):
    route_segments = [generate_route_segment(), generate_route_segment()]

    db_route_segments = get_route_segments()

    assert 2 == len(db_route_segments)
    assert route_segments == db_route_segments


def test_create_route_segment():
    route_segment = make_route_segment(POINT_TYPE.DESIGNATED_POINT)

    db_route_segment = create_route_segment(route_segment)

    assert isinstance(db_route_segment, RouteSegment)
    assert isinstance(db_route_segment.identifier, str)
    assert route_segment.identifier == db_route_segment.identifier


def test_update_route_segment(generate_route_segment):
    route_segment = generate_route_segment()

    route_segment.name = 'new name'

    updated_route_segment = update_route_segment(route_segment)

    assert isinstance(updated_route_segment, RouteSegment)
    assert 'new name' == updated_route_segment.name


def test_delete_route_segment(generate_route_segment):
    route_segment = generate_route_segment()

    delete_route_segment(route_segment)

    assert get_route_segment_by_id(route_segment.identifier) is None
