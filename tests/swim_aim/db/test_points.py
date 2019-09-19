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
from swim_aim.db.models import Point, POINT_TYPE
from swim_aim.db.points import get_point_by_id, get_points, create_point, \
    update_point, delete_point
from tests.swim_aim.db.utils import make_point

__author__ = "EUROCONTROL (SWIM)"


@pytest.fixture
def generate_point(session):
    def _generate_point(point_type=POINT_TYPE.DESIGNATED_POINT):
        point = make_point(point_type)
        return db_save(session, point)

    return _generate_point


def test_get_point_by_id__does_not_exist__returns_none():
    assert get_point_by_id('1111') is None


def test_get_point_by_id__object_exists_and_is_returned(generate_point):
    point = generate_point()

    db_point = get_point_by_id(point.identifier)

    assert isinstance(db_point, Point)
    assert point.identifier == db_point.identifier


def test_get_points__no_point_in_db__returns_empty_list(generate_point):
    db_points = get_points()

    assert [] == db_points


def test_get_points__existing_points_are_returned(generate_point):
    points = [generate_point(), generate_point()]

    db_points = get_points()

    assert 2 == len(db_points)
    assert points == db_points


def test_get_points__filter_by_point_type(generate_point):
    generate_point(POINT_TYPE.NAVAID)
    generate_point(point_type=POINT_TYPE.DESIGNATED_POINT)

    db_points = get_points(point_type=POINT_TYPE.NAVAID.value)

    assert 1 == len(db_points)
    assert POINT_TYPE.NAVAID == db_points[0].point_type


def test_create_point():
    point = make_point(POINT_TYPE.NAVAID)

    db_point = create_point(point)

    assert isinstance(db_point, Point)
    assert isinstance(db_point.identifier, str)
    assert point.identifier == db_point.identifier


def test_update_point(generate_point):
    point = generate_point()

    point.name = 'new name'

    updated_point = update_point(point)

    assert isinstance(updated_point, Point)
    assert 'new name' == updated_point.name


def test_delete_point(generate_point):
    point = generate_point()

    delete_point(point)

    assert get_point_by_id(point.identifier) is None
