from django.test.runner import DiscoverRunner  as TestRunner


class DjangoTestSuiteRunner(TestRunner):
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
