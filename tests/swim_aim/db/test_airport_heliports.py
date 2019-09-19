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
from swim_aim.db.models import AirportHeliport
from swim_aim.db.airport_heliports import get_airport_heliport_by_id, get_airport_heliports, create_airport_heliport, \
    update_airport_heliport, delete_airport_heliport
from tests.swim_aim.db.utils import make_airport_heliport

__author__ = "EUROCONTROL (SWIM)"


@pytest.fixture
def generate_airport_heliport(session):
    def _generate_airport_heliport():
        airport_heliport = make_airport_heliport()
        return db_save(session, airport_heliport)

    return _generate_airport_heliport


def test_get_airport_heliport_by_id__does_not_exist__returns_none():
    assert get_airport_heliport_by_id('1111') is None


def test_get_airport_heliport_by_id__object_exists_and_is_returned(generate_airport_heliport):
    airport_heliport = generate_airport_heliport()

    db_airport_heliport = get_airport_heliport_by_id(airport_heliport.identifier)

    assert isinstance(db_airport_heliport, AirportHeliport)
    assert airport_heliport.identifier == db_airport_heliport.identifier


def test_get_airport_heliports__no_airport_heliport_in_db__returns_empty_list(generate_airport_heliport):
    db_airport_heliports = get_airport_heliports()

    assert [] == db_airport_heliports


def test_get_airport_heliports__existing_airport_heliports_are_returned(generate_airport_heliport):
    airport_heliports = [generate_airport_heliport(),
                         generate_airport_heliport()]

    db_airport_heliports = get_airport_heliports()

    assert 2 == len(db_airport_heliports)
    assert airport_heliports == db_airport_heliports


def test_create_airport_heliport():
    airport_heliport = make_airport_heliport()

    db_airport_heliport = create_airport_heliport(airport_heliport)

    assert isinstance(db_airport_heliport, AirportHeliport)
    assert isinstance(db_airport_heliport.identifier, str)
    assert airport_heliport.identifier == db_airport_heliport.identifier


def test_update_airport_heliport(generate_airport_heliport):
    airport_heliport = generate_airport_heliport()

    airport_heliport.name = 'new name'

    updated_airport_heliport = update_airport_heliport(airport_heliport)

    assert isinstance(updated_airport_heliport, AirportHeliport)
    assert 'new name' == updated_airport_heliport.name


def test_delete_airport_heliport(generate_airport_heliport):
    airport_heliport = generate_airport_heliport()

    delete_airport_heliport(airport_heliport)

    assert get_airport_heliport_by_id(airport_heliport.identifier) is None
