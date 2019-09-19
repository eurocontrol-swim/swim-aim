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
from swim_aim.db.models import Route
from swim_aim.db.routes import get_route_by_id, get_routes, create_route, \
    update_route, delete_route
from tests.swim_aim.db.utils import make_route

__author__ = "EUROCONTROL (SWIM)"


@pytest.fixture
def generate_route(session):
    def _generate_route():
        route = make_route()
        return db_save(session, route)

    return _generate_route


def test_get_route_by_id__does_not_exist__returns_none():
    assert get_route_by_id('1111') is None


def test_get_route_by_id__object_exists_and_is_returned(generate_route):
    route = generate_route()

    db_route = get_route_by_id(route.identifier)

    assert isinstance(db_route, Route)
    assert route.identifier == db_route.identifier


def test_get_routes__no_route_in_db__returns_empty_list(generate_route):
    db_routes = get_routes()

    assert [] == db_routes


def test_get_routes__existing_routes_are_returned(generate_route):
    routes = [generate_route(),
                         generate_route()]

    db_routes = get_routes()

    assert 2 == len(db_routes)
    assert routes == db_routes


def test_create_route():
    route = make_route()

    db_route = create_route(route)

    assert isinstance(db_route, Route)
    assert isinstance(db_route.identifier, str)
    assert route.identifier == db_route.identifier


def test_update_route(generate_route):
    route = generate_route()

    route.name = 'new name'

    updated_route = update_route(route)

    assert isinstance(updated_route, Route)
    assert 'new name' == updated_route.name


def test_delete_route(generate_route):
    route = generate_route()

    delete_route(route)

    assert get_route_by_id(route.identifier) is None
