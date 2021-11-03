from flask import Flask, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from utopia.models.flights import FLIGHT_SCHEMA, Flight, Route, Airport, FlightSchema, FLIGHT_SCHEMA_MANY, ROUTE_SCHEMA, ROUTE_SCHEMA_MANY, AIRPORT_SCHEMA, AIRPORT_SCHEMA_MANY,FlightBookings

from utopia.models.booking import BOOKING_SCHEMA_FULL, BOOKING_SCHEMA_FULL_MANY,  Booking, BookingPayment, BookingSchemaFull, Passenger, BOOKING_SCHEMA, BOOKING_SCHEMA_MANY, PASSENGER_SCHEMA, PASSENGER_SCHEMA_MANY, FLIGHT_BOOKINGS_SCHEMA, FLIGHT_BOOKINGS_SCHEMA_MANY, BOOKING_PAYMENT_SCHEMA

from utopia.models.users import USER_ROLE_SCHEMA, USER_SCHEMA_MANY, BookingUser, BookingAgent, BookingGuest, BOOKING_GUEST_SCHEMA, USER_SCHEMA, BOOKING_AGENT_SCHEMA, User, BOOKING_USER_SCHEMA, BOOKING_AGENT_SCHEMA,BOOKING_USER_SCHEMA, UserRole, UserSchema


from flask_jwt_extended import create_access_token



from utopia.models.base import db_session
from utopia import app
from sqlalchemy.exc import IntegrityError
import logging, datetime
logging.basicConfig(level=logging.INFO)

bcrypt = Bcrypt(app)

class UserService:

##################### GET #####################

    def read_users(self):
        logging.info('reading all users')

        users = db_session.query(User).all()

        users = jsonify({'users': USER_SCHEMA_MANY.dump(users)})
        db_session.close()

        return users

    def find_user(self, id):
        logging.info('finding user with id %s' %id)

        user = db_session.query(User).get(id)

        db_session.commit()
        user = USER_SCHEMA.dump(user)
        db_session.close()

        return user

    def find_user_by_username(self, username):
        logging.info('finding user with username %s' %username)

        user = db_session.query(User).filter_by(username=username).first()

        db_session.commit()
        user = USER_SCHEMA.dump(user)
        db_session.close()

        return user

    def read_user_by_role(self, id):

        logging.info('reading all users with id %s' %id)
        
        users = db_session.query(User).filter_by(role_id=id)

        users = jsonify({'users' : USER_SCHEMA_MANY.dump(users)})
        db_session.close()
        return users

    
    

##################### POST #####################

    def login_user(self, username, password):

        user = db_session.query(User).filter_by(username=username).first()

        db_session.close()
        if not user:  
            return False

        if  bcrypt.check_password_hash(user.password, password):
            return True

        return False

    def add_user(self, user):
        logging.info('adding new user')


        user_to_add = User(given_name = user['given_name'],
                            family_name = user['family_name'],
                            role_id = user['role_id'],
                            username = user['username'],
                            email = user['email'],
                            password = bcrypt.generate_password_hash(user['password']),
                            phone =user['phone']
        )
        db_session.add(user_to_add)


        db_session.commit()

        user = USER_SCHEMA.dump(user_to_add)
        db_session.close()

        return user


    def add_user_role(self, user_role):
        logging.info('adding user role')

        user_role_to_add = UserRole(id=user_role['id'], name=user_role['name'])
        db_session.add(user_role_to_add)

        db_session.commit()
        user_role = USER_ROLE_SCHEMA.dump(user_role_to_add)
        db_session.close()
        return user_role



##################### PUT #####################


    def update_user(self, user):
        logging.info('updating user')

        user_to_update = db_session.query(User).get(user['id'])

        if 'role_id' in user:
            user_to_update.role_id = user['role_id']
        if 'given_name' in user:
            user_to_update.given_name = user['given_name']
        if 'family_name' in user:
            user_to_update.family_name = user['family_name']
        if 'username' in user:
            user_to_update.username = user['username']
        if 'email'  in user:
            user_to_update.email = user['email']
        if 'password' in user:
            user_to_update.password = bcrypt.generate_password_hash(user['password'])
        if 'phone' in user:
            user_to_update.phone = user['phone']

        db_session.commit()

        user = USER_SCHEMA.dump(user_to_update)
        db_session.close()
        return user

    def update_user_role(self, user_role):
        logging.info('update user role')

        user_role_to_update = db_session.query(UserRole).get(user_role['id'])
        if 'name' in user_role:
            user_role_to_update.name = user_role['name']

        db_session.commit()

        user_role = USER_ROLE_SCHEMA.dump(user_role_to_update)
        db_session.close()
        return user_role



##################### DELETE #####################

    def delete_user(self, id):
        logging.info('delete user with id %s' %id)


        user = db_session.query(User).get(id)
        db_session.delete(user)

        db_session.commit()
        db_session.close()
        return ''

    def delete_user_role(self, id):
        logging.info('delete user role with id %s' %id)


        user_role = db_session.query(UserRole).get(id)
        db_session.delete(user_role)

        db_session.commit()
        db_session.close()
        return ''       
