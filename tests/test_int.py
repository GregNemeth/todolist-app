from os import name
from flask_testing import LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen
from flask import url_for
from application import app, db
from application.models import Tasks

class TestBase(LiveServerTestCase):
    TEST_PORT = 5050

    def create_app(self):
        

        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            LIVESERVER_PORT=self.TEST_PORT,
            WTF_CSRF_ENABLED=False,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            DEBUG=True,
            TESTING=True
        )

        return app

    def setUp(self):
        db.create_all()

        db.session.add(Tasks(name='Run unit tests'))
        db.session.add(Tasks(name='Do something else',done=True))

        db.session.commit()

        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=chrome_options)

        

        self.driver.get(f'http://localhost:{self.TEST_PORT}')

    def tearDown(self):

        self.driver.quit()

        db.drop_all()

    def test_server_is_up_and_running(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}')
        self.assertEqual(response.code, 200)

class TestCreate(TestBase):
    def test_create(self):
        # navigate to create page
        self.driver.find_element_by_xpath('/html/body/div/a').click()
        # find and populate text box
        self.driver.find_element_by_xpath('//*[@id="name"]').send_keys('Check create form')
        # find and click submit button
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        # check history
        element = self.driver.find_element_by_xpath('/html/body/div[4]')
        assert 'Check create form' in element.text