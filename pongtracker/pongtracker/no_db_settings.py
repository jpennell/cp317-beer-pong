from pongtracker.settings import *
# Test runner with no database creation
TEST_RUNNER = 'testing.testrunner.NoDbTestRunner'


# Use an alternative database as a safeguard against accidents
DATABASES['default']['NAME'] = 'testblac2410'