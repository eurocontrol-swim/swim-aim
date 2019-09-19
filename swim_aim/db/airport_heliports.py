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
from typing import Union, List

from sqlalchemy.orm.exc import NoResultFound
from swim_backend.db import db_save, db, db_delete

from swim_aim.db.models import AirportHeliport

__author__ = "EUROCONTROL (SWIM)"


def get_airport_heliport_by_id(airport_heliport_id: str) -> Union[AirportHeliport, None]:
    """
    Retrieves an AirportHeliport object provided its identifier from DB.

    :param airport_heliport_id:
    :return:
    """
    try:
        result = AirportHeliport.query.filter_by(identifier=airport_heliport_id).one()
    except NoResultFound:
        result = None

    return result


def get_airport_heliports() -> List[AirportHeliport]:
    """
    Retrieves all the AirportHeliport objects from DB.
    :return:
    """
    return AirportHeliport.query.all()


def create_airport_heliport(airport_heliport: AirportHeliport) -> AirportHeliport:
    """
    Creates a new AirportHeliport object in DB.
    :param airport_heliport:
    :return:
    """
    return db_save(db.session, airport_heliport)


def update_airport_heliport(airport_heliport: AirportHeliport) -> AirportHeliport:
    """
    Updates an AirportHeliport object in DB.
    :param airport_heliport:
    :return:
    """
    return db_save(db.session, airport_heliport)


def delete_airport_heliport(airport_heliport: AirportHeliport) -> None:
    """
    Deletes an AirportHeliport object from DB.

    :param airport_heliport:
    """
    db_delete(db.session, airport_heliport)
