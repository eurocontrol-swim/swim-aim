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
import enum

from swim_backend.db import db

__author__ = "EUROCONTROL (SWIM)"


class BaseModel(db.Model):
    __abstract__ = True

    def _dict(self):
        return {key: value for key, value in self.__dict__.items() if key not in ['_sa_instance_state']}

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._dict() == other._dict()

    def __ne__(self, other) -> bool:
        return not other == self


class AirportHeliport(BaseModel):

    __tablename__ = 'airport_heliports'

    identifier = db.Column(db.String, primary_key=True)

    interpretation = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    icao_location_indicator = db.Column(db.String, nullable=False)
    iata_designator = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    control_type = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    srs_name = db.Column(db.String)
    elevation = db.Column(db.Float)
    elevation_uom = db.Column(db.String)
    begin_lifetime = db.Column(db.DateTime)
    end_lifetime = db.Column(db.DateTime)


class POINT_TYPE(enum.Enum):
    NAVAID = "NAVAID"
    DESIGNATED_POINT = "DESIGNATED_POINT"


class Point(BaseModel):

    __tablename__ = 'points'

    identifier = db.Column(db.String, primary_key=True)

    interpretation = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    designator = db.Column(db.String)
    type = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    srs_name = db.Column(db.String)
    elevation = db.Column(db.Float)
    elevation_uom = db.Column(db.String)
    begin_lifetime = db.Column(db.DateTime)
    end_lifetime = db.Column(db.DateTime)
    point_type = db.Column(db.Enum(POINT_TYPE), nullable=False)


class Route(BaseModel):

    __tablename__ = 'routes'

    identifier = db.Column(db.String, primary_key=True)

    interpretation = db.Column(db.String, nullable=False)
    designator_prefix = db.Column(db.String)
    designator_second_letter = db.Column(db.String)
    designator_number = db.Column(db.Integer)
    type = db.Column(db.String, nullable=False)
    begin_lifetime = db.Column(db.DateTime)
    end_lifetime = db.Column(db.DateTime)

    segments = db.relationship("RouteSegment", back_populates="route")


class RouteSegment(BaseModel):

    __tablename__ = 'route_segments'

    identifier = db.Column(db.String, primary_key=True)
    start = db.Column(db.String, db.ForeignKey(Point.identifier), nullable=False)
    end = db.Column(db.String, db.ForeignKey(Point.identifier), nullable=False)
    route_formed = db.Column(db.String, db.ForeignKey(Route.identifier), nullable=False)

    interpretation = db.Column(db.String, nullable=False)
    upper_limit = db.Column(db.String)
    upper_limit_uom = db.Column(db.String)
    upper_limit_ref = db.Column(db.String)
    lower_limit = db.Column(db.String)
    lower_limit_uom = db.Column(db.String)
    lower_limit_ref = db.Column(db.String)
    begin_lifetime = db.Column(db.DateTime)
    end_lifetime = db.Column(db.DateTime)

    route = db.relationship("Route", back_populates="segments")
    start_point = db.relationship("Point", foreign_keys=[start])
    end_point = db.relationship("Point", foreign_keys=[end])
