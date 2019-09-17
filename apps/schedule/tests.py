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

    def test_set_nagruzka(self):
        r = self.client.post("/api/brix/set_nagruzka/", {
            "raspnagr_id": 4259584,
            "date": "2019-09-03",
            "pair": 3,
        })
        print(r.json())
