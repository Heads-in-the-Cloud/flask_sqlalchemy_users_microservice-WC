import unittest
from flask import Flask, json, jsonify

from utopia import app
import random
from sqlalchemy.exc import IntegrityError, OperationalError
from utopia.user_service import UserService

from utopia.user_controller import USER_SERVICE


ROLE_DICT = {1: 'ROLE_ADMIN', 2: 'ROLE_AGENT', 3: 'ROLE_TRAVELER'}


FLIGHT_ID = 1
AGENT_ID=1
USER_ID = 33
GUEST = 'guest'

ADMIN_USERNAME = 'admin101010101010101010101'
AGENT_USERNAME = 'agent101010101010101010101'
TRAVELER_USERNAME = 'traveler101010101010101010101'

ADMIN = 1
AGENT = 2
TRAVELER = 3
NEW_ROLE = 'ROLE_CAPTAIN'
ROLE_ID = 100

class TestBooking(unittest.TestCase):


    @classmethod
    def setUpClass(cls):

        print('set up class')

        with app.app_context():

            print('set up user')
            user = {'given_name' : 'Mr. Admin', 'role_id': ADMIN, 'family_name' : 'Admin', 'username' : ADMIN_USERNAME, 'password' : 'pass',
           'phone' : '555 555 5555', 'email' : ADMIN_USERNAME+'@gmail.com'}

            USER_SERVICE.add_user(user)

            user['role_id'] = AGENT
            user['given_name'] = 'Mr. Agent'
            user['username'] = AGENT_USERNAME
            user['email'] = AGENT_USERNAME+'@gmail.com'
            user['phone'] = '444 444 4444'
            USER_SERVICE.add_user(user)

            user['role_id'] = TRAVELER
            user['given_name'] = 'Mr. Traveler'
            user['username'] = TRAVELER_USERNAME
            user['email'] = TRAVELER_USERNAME+'@gmail.com'
            user['phone'] = '333 333 3333'
            
            USER_SERVICE.add_user(user)


            print('set up user role')
            user_role = {'id' : ROLE_ID, 'name' : NEW_ROLE}
            USER_SERVICE.add_user_role(user_role)


    @classmethod
    def tearDownClass(cls):
        print('tear down class')

        with app.app_context():  
            print('tear down users')  
            admin_id = USER_SERVICE.find_user_by_username(ADMIN_USERNAME)['id']
            agent_id = USER_SERVICE.find_user_by_username(AGENT_USERNAME)['id']
            traveler_id = USER_SERVICE.find_user_by_username(TRAVELER_USERNAME)['id']

            USER_SERVICE.delete_user(admin_id)
            USER_SERVICE.delete_user(agent_id)
            USER_SERVICE.delete_user(traveler_id)

            print('tear down role')
            USER_SERVICE.delete_user_role(ROLE_ID)


    def test_read_users(self):
        with app.app_context():

            users = USER_SERVICE.read_users().json['users']

            for user in users:
                self.assertEqual(user['user_role']['name'], ROLE_DICT[user['role_id']])

    def test_find_user_wrong_id(self):
        with app.app_context():

                user = USER_SERVICE.find_user(0)
                self.assertEqual(user, {})

    def test_find_user_null_username(self):
        with app.app_context():

            user = USER_SERVICE.find_user_by_username(None)
            
            self.assertEqual(user, {})  

    def test_update_user(self):
        with app.app_context():

            user = USER_SERVICE.find_user_by_username(ADMIN_USERNAME)
            user = {'id':user['id'], 'given_name' : 'John', 'family_name' : 'Doe', 'username':'JohnDoe101010101010'}
            updated_user = USER_SERVICE.update_user(user)
            self.assertEqual(user['given_name'], updated_user['given_name'])
            self.assertEqual(user['family_name'], updated_user['family_name'])
            self.assertEqual(user['username'], updated_user['username'])

            updated_user['username'] = ADMIN_USERNAME
            USER_SERVICE.update_user(updated_user)

    def test_update_user_role(self):
        with app.app_context():

            user = USER_SERVICE.find_user_by_username(ADMIN_USERNAME)

            user['role_id'] = ROLE_ID

            updated_user = USER_SERVICE.update_user(user)
            self.assertEqual(updated_user['user_role']['name'], NEW_ROLE)

    def test_update_role(self):
        with app.app_context():

            user_role = {'id' : ROLE_ID, 'name' : 'ROLE STEWARD'}

            updated_user_role = USER_SERVICE.update_user_role(user_role)

            self.assertEqual(updated_user_role['name'], user_role['name'])
            updated_user_role['name'] = NEW_ROLE
            
            USER_SERVICE.update_user_role(updated_user_role)




         









