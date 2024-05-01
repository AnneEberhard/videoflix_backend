import subprocess
from django.test.runner import DiscoverRunner


# change in settings.py: TEST_RUNNER = 'tests.flake8_test.Flake8TestRunner'

class Flake8TestRunner(DiscoverRunner):
    def run_tests(self, test_labels, **kwargs):
        # Run Flake8 before running tests
        flake8_result = subprocess.run(['flake8', 'videoflix/'], stdout=subprocess.PIPE)
        print(flake8_result.stdout.decode('utf-8'))
        # Run the tests using the standard Django test runner
        return super().run_tests(test_labels, **kwargs)

