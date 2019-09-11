from pprint import pprint

from django.test import TestCase

# Create your tests here.
from BrixSchedule.tests import TestCaseBase


class TestBrixViewset(TestCaseBase):
    def test_get_nagruzka(self):
        r = self.client.get("/api/brix/nagruzka/")
        pprint(r.json())

    def test_get_konts(self):
        r = self.client.get("/api/brix/konts/")
        pprint(r.json())

