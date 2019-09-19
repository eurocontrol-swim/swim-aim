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
from typing import Union, List, Optional

from sqlalchemy.orm.exc import NoResultFound
from swim_backend.db import db_save, db, db_delete

from swim_aim.db.models import Point

__author__ = "EUROCONTROL (SWIM)"


def get_point_by_id(point_id: str) -> Union[Point, None]:
    """
    Retrieves an Point object provided its identifier from DB.

    :param point_id:
    :return:
    """
    try:
        result = Point.query.filter_by(identifier=point_id).one()
    except NoResultFound:
        result = None

    return result


def get_points(point_type: Optional[str] = None) -> List[Point]:
    """
    Retrieves all the Point objects from DB. Optionally they can be filtered based on their point_type,
    .i.e NAVAID, DESIGNATED_POINT
    :param point_type:
    :return:
    """
    filters = {}

    if point_type is not None:
        filters['point_type'] = point_type

    return Point.query.filter_by(**filters).all()


def create_point(point: Point) -> Point:
    """
    Creates a new Point object in DB.
    :param point:
    :return:
    """
    return db_save(db.session, point)


def update_point(point: Point) -> Point:
    """
    Updates an Point object in DB.
    :param point:
    :return:
    """
    return db_save(db.session, point)


def delete_point(point: Point) -> None:
    """
    Deletes an Point object from DB.

    :param point:
    """
    db_delete(db.session, point)
