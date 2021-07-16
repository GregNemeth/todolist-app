
from os import name
from flask.helpers import url_for
from flask.scaffold import F
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase

from application import app, db
from application.models import Tasks

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

        db.session.add(Tasks(name='Run unit tests'))
        db.session.add(Tasks(name='Do something else'))
        
        db.session.commit()

    def tearDown(self):
        db.drop_all

class TestViews(TestBase):
    def test_home(self):
        response = self.client.get(url_for('home'))
        self.assert200(response)

    def test_create(self):
        response = self.client.get(url_for('create'))
        self.assert200(response)

    def test_update(self):
        response = self.client.get(url_for('update', id=1))
        self.assert200(response)

    def test_delete_task(self):
        response = self.client.get(url_for('delete_task', id=2))
        self.assertEqual(response.status_code, 302)

    def test_completed(self):
        response = self.client.get(url_for('completed', id=1))
        self.assertEqual(response.status_code, 302)

    def test_incomplete(self):
        response = self.client.get(url_for('incomplete', id=1))
        self.assertEqual(response.status_code, 302)

    def test_donedem(self):
        response = self.client.get(url_for('donedem', id=1))
        self.assertEqual(response.status_code, 200)

class TestRead(TestBase):
    def test_home(self):
        response = self.client.get(url_for('home'))

        assert "Run unit test" in response.data.decode()
        assert "Do something else" in response.data.decode()

class TestCreate(TestBase):
    def test_create(self):
        response = self.client.post(
            url_for('create'),
            data={'name':'Check create is working'},
            follow_redirects=True
            )

        assert 'Check create is working' in response.data.decode()

class TestUpdate(TestBase):
    def test_update(self):
        response = self.client.post(
            url_for('update', id=1),
            data={'name':'Check if update is working'},
            follow_redirects=True
            )

        assert 'Check if update is working' in response.data.decode()
        assert 'Run unit tests' not in response.data.decode()

class TestDelete(TestBase):
    def test_delete(self):
        response = self.client.get(
            url_for('delete_task', id=2),
            follow_redirects=True
        )

        assert 'Do something else' not in response.data.decode()

class TestCompleted(TestBase):
    def test_completed(self):
        response = self.client.get(
            url_for('completed', id=1),
            follow_redirects=True
        )

        assert '1 - Run unit tests - True' in response.data.decode()