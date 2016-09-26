import os
import unittest
from provdbconnector.databases import Neo4jAdapter
from provdbconnector.databases import InvalidOptionsException, AuthException
from tests.databases.test_baseadapter import AdapterTestTemplate

test_user_name = os.environ.get('NEO4J_USERNAME', 'neo4j')
test_user_pass = os.environ.get('NEO4J_PASSWORD', 'neo4jneo4j') #Password
test_host =  os.environ.get('NEO4J_HOST', 'localhost:7687')

class Neo4jAdapterTests(AdapterTestTemplate):

    def setUp(self):
        self.instance = Neo4jAdapter()
        authInfo = dict()
        authInfo.update({"user_name": test_user_name})
        authInfo.update({"user_password":test_user_pass})
        authInfo.update({"host": test_host})

        self.instance.connect(authInfo)

    def test_connect(self):
        authInfo = dict()
        authInfo.update({"user_name": "neo4j"})
        authInfo.update({"user_password": "neo4jneo4j"})
        authInfo.update({"host": test_host})
        self.instance.connect(authInfo)

    def test_connect_fails(self):
        authInfo = dict()
        authInfo.update({"user_name": "neo4j"})
        authInfo.update({"user_password": "xxxxxxxxxx"})
        authInfo.update({"host": test_host})
        self.instance.connect(authInfo)
        with self.assertRaises(AuthException):
            self.instance.connect(authInfo)

    def test_connect_invalid_options(self):
        authInfo = dict()
        authInfo.update({"xxxx": "neo4j"})
        authInfo.update({"xx": "neo4jneo4j"})
        authInfo.update({"xx": test_host})

        with self.assertRaises(InvalidOptionsException):
            self.instance.connect(authInfo)

    def test_create_document_id_increment(self):
        first= self.instance.create_document()

        first= int(first)

        second = self.instance.create_document()
        second = int(second)

        self.assertEqual(first+1,second)

    def tearDown(self):
        session = self.instance._create_session()
        session.run("MATCH (x) DETACH DELETE x")
        del self.instance
