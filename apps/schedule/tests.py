from datetime import datetime
from pprint import pprint

from model_mommy import mommy

from BrixSchedule.tests import TestCaseBase
from apps.schedule.models import BrixModule, Kontkurs


class TestBrixViewset(TestCaseBase):
    def test_get_nagruzka(self):
        r = self.client.get("/api/brix/nagruzka/")
        pprint(r.json())

    def test_get_konts(self):
        r = self.client.get("/api/brix/konts/")
        pprint(r.json())

    def test_get_raspis(self):
        r = self.client.get("/api/brix/raspis/")
        pprint(r.json())

    def test_set_nagruzka(self):
        r = self.client.post("/api/brix/set_nagruzka/", {
            "raspnagr_id": 4259584,
            "date": "2019-09-03",
            "pair": 3,
        })
        print(r.json())


class TestBrixModulesViewset(TestCaseBase):
    def test_get_for_kont(self):
        kontkurs = mommy.make(Kontkurs, title="kont")
        module1 = mommy.make(BrixModule, kont=kontkurs)
        module2 = mommy.make(BrixModule, kont=kontkurs)
        module3 = mommy.make(BrixModule, kont=kontkurs)

        r = self.client.get("/api/brix-modules/get-for-kont/", {
            "kont_id": kontkurs.id
        })
        pprint(r.json())

    def test_hours_for_konts(self):
        kontkurs = mommy.make(Kontkurs, title="kont")
        module = mommy.make(BrixModule, kont=kontkurs)

        r = self.client.get("/api/brix-modules/get-hours-for-kont/", {
            "kont_id": kontkurs.id
        })
        pprint(r.json())

    def test_update_or_create(self):
        r = self.client.post("/api/brix-modules/update-or-create/", {
            "kont_id": 120,
            "date_start": "2019-09-01",
            "date_end": "2019-09-30",
            "title": "module 1",
        })
        data = r.json()

        r = self.client.post("/api/brix-modules/update-or-create/", {
            "id": data['id'],
            "kont_id": 121,
            "date_start": "2019-09-10",
            "date_end": "2019-09-25",
            "title": "module 2",
        })

        module = BrixModule.objects.get(id=data['id'])
        self.assertEqual(121, module.kont_id)
        self.assertEqual("module 2", module.title)
        self.assertEqual(datetime(2019, 9, 10), module.date_start)
        self.assertEqual(datetime(2019, 9, 25), module.date_end)

        r = self.client.delete("/api/brix-modules/remove/", {
            "id": module.id,
        })

        self.assertEqual(0, BrixModule.objects.filter(id=module.id).count())
