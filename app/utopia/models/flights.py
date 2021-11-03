from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from sqlalchemy.sql.sqltypes import Float
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import backref, relation, relationship
from utopia import app
from utopia.models.base import Base, db_session


ma = Marshmallow(app)

def generate_f_id():
    

    flight_ids = db_session.execute('SELECT id FROM flight')
    i=1
    for id in flight_ids:
        
        if i == id[0]:
            i+=1
        else:
            break
    db_session.close()
    return i


class Flight(Base):
    __tablename__ = 'flight'

    id = Column(Integer, primary_key=True, default=generate_f_id)
    route_id = Column(Integer, ForeignKey('route.id'))
    airplane_id = Column(Integer, ForeignKey('airplane.id'))
    departure_time = Column(DateTime)
    reserved_seats = Column(Integer)
    seat_price = Column(Float(precision=None, decimal_return_scale=2))
    flight_bookings = relationship("FlightBookings", backref='flight', lazy='subquery', cascade='all, delete')


class Airport(Base):
    __tablename__ = 'airport'


    iata_id = Column(String(3), primary_key=True)
    city =  Column(String(45))
    outgoing = relationship("Route", lazy='subquery', primaryjoin="Airport.iata_id == Route.origin_id")
    incoming = relationship("Route", lazy='subquery', primaryjoin="Airport.iata_id == Route.destination_id")


class Route(Base):
    __tablename__ = 'route'


    id = Column(Integer, primary_key=True)
    destination_id = Column(String(3) , ForeignKey("airport.iata_id"))
    origin_id =  Column(String(3) , ForeignKey("airport.iata_id"))
    flights = relationship('Flight', backref='route', lazy='subquery', cascade='all, delete')
    origin_airport = relationship("Airport", primaryjoin="Airport.iata_id == Route.origin_id")
    destination_airport = relationship("Airport", primaryjoin="Airport.iata_id == Route.destination_id")


class AirplaneType(Base):
    __tablename__ = 'airplane_type'

    id = Column(Integer, primary_key=True)
    max_capacity = Column(Integer)
    airplanes = relationship("Airplane", lazy='subquery', cascade='all, delete', backref="airplane_type")



class Airplane(Base):
    __tablename__ = 'airplane'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey(AirplaneType.id))
    flights = relationship("Flight", lazy='subquery', cascade='all, delete', backref='airplane')

class FlightBookings(Base):
    __tablename__ = 'flight_bookings'

    booking_id = Column(Integer, ForeignKey('booking.id'), primary_key=True)
    flight_id = Column(Integer, ForeignKey('flight.id'))




######################################## SCHEMAS ########################################



   
class AirportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        Base = Airport
        ordered = True
        fields = ('iata_id', 'city')



class RouteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        Base = Route
        ordered = True
        fields = ('id', 'origin_id', 'destination_id', 'origin_airport', 'destination_airport')
    origin_airport = fields.Nested(AirportSchema, only=['city'])
    destination_airport = fields.Nested(AirportSchema, only=['city'])


class AirplaneTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        Base = AirplaneType
        ordered = True
        fields = ('id', 'max_capacity')



class AirplaneSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        Base = Airplane
        fields = ('id', 'type_id')
        ordered = True
    airplane_type = fields.Nested(AirplaneTypeSchema, only=["max_capacity"])


class FlightSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        Base = Flight
        fields = ("id", "route_id", "route", "airplane_id", "departure_time", "reserved_seats", "seat_price")
        ordered = True
    route = fields.Nested(RouteSchema, only = ['origin_id', 'destination_id'])


class FlightBookingsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FlightBookings
        fields = ('booking_id', 'flight_id', 'flight')
    flight = fields.Nested(FlightSchema, exclude=['id', 'route_id'])

AIRPORT_SCHEMA = AirportSchema()
ROUTE_SCHEMA = RouteSchema()
AIRPLANE_TYPE_SCHEMA = AirplaneTypeSchema()
AIRPLANE_SCHEMA = AirplaneSchema()

AIRPORT_SCHEMA_MANY = AirportSchema(many=True)
ROUTE_SCHEMA_MANY = RouteSchema(many=True)
AIRPLANE_TYPE_SCHEMA_MANY = AirplaneTypeSchema(many=True)
AIRPLANE_SCHEMA_MANY = AirplaneSchema(many=True)

FLIGHT_SCHEMA_MANY = FlightSchema(many=True)
FLIGHT_SCHEMA = FlightSchema()
