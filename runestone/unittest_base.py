import unittest
import os
import subprocess
from selenium import webdriver

# Select an unused port for serving web pages to the test suite.
PORT = '8081'

# Define `module modules fixtures <https://docs.python.org/2/library/unittest.html#setupmodule-and-teardownmodule>`_ to build the test Runestone project, run the server, then shut it down when the tests complete.
class ModuleFixture(object):
    def __init__(self,
        # The path to the Python module in which the test resides. This provides a simple way to determine the path in which to run runestone build/serve.
        module_path):

        super(ModuleFixture, self).__init__()
        self.base_path = os.path.dirname(module_path)

    def setUpModule(self):
        # Change to this directory for running Runestone.
        self.old_cwd = os.getcwd()
        os.chdir(self.base_path)
        # Compile the docs.
        subprocess.check_call(['runestone', 'build', '--all'])
        # Run the server. Simply calling ``runestone serve`` fails, since the process killed isn't the actual server, but probably a setuptools-created launcher.
        self.runestone_server = subprocess.Popen(['python', '-m', 'runestone', 'serve', '--port', PORT])

    def tearDownModule(self):
        # Shut down the server.
        self.runestone_server.kill()
        # Restore the directory.
        os.chdir(self.old_cwd)

# Provide a simple way to instantiante a ModuleFixture in a test module. Typical use:
#
# .. code:: Python
#   :number-lines:
#
#   from unittest_base import module_fixture_maker
#   setUpModule, tearDownModule = module_fixture_maker(__file__)
def module_fixture_maker(module_path):
    mf = ModuleFixture(module_path)
    return mf.setUpModule, mf.tearDownModule

# Provide a base test case which sets up the `Selenium <http://selenium-python.readthedocs.io/>`_ driver.
class RunestoneTestCase(unittest.TestCase):
    def setUp(self):

        #self.driver = webdriver.PhantomJS() # use this for Jenkins auto testing
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1200x800")
        self.driver = webdriver.Chrome(chrome_options=options)  # good for development.


        self.host = 'http://127.0.0.1:' + PORT

    def tearDown(self):
        self.driver.quit()

