from itertools import groupby

from django.db.models.expressions import RawSQL
from django.views import View
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.schedule.consts import BRIX_FACULTY_ID
from apps.schedule.models import Raspnagr, RaspisZaoch, Kontkurs
from apps.schedule.utils import kont_obozn_process


class BrixViewSet(ViewSet):
    def get_semester(self):
        return 1

    def get_weeks_count(self):
        return 16

    @action(detail=False)
    def konts(self, request):
        query = Kontkurs.objects.filter(id__in=RawSQL("""
        SELECT kk.id_1
        FROM raspnagr rn
         LEFT JOIN kontgrp kg ON kg.id_7 = rn.kontid
         LEFT JOIN kontlist kl ON kl.op = rn.op
         LEFT JOIN kontkurs kk ON kk.id_1 = isnull(kl.kont, rn.kont)
        WHERE kk.fac = %(fac)s and rn.sem = %(sem)s
        """ % {
            "fac": BRIX_FACULTY_ID,
            "sem": self.get_semester(),
        }, []))

        result = {
            i.id: {
                'title': kont_obozn_process(i.title)
            } for i in query
        }

        return Response(result)

    @action(detail=False)
    def nagruzka(self, request):
        query = """
SELECT rn.id_51 as id_51, 
    rtrim(coalesce(pl.konts, kg.obozn, kk.obozn)) as grp, 
    rtrim(kk.obozn) as kont,
    rtrim(kg.obozn) as kont_group,
    kk.id_1 as kont_id,
    kg.id_7 as kont_group_id,
    kk.kurs,
    rn.op as op,
    rn.nt as nt,
    rn.prep as prep,
    rtrim(vp.pred) as pred,
    hy1 * %(weeks_count)s as hours
FROM raspnagr rn
 LEFT JOIN kontgrp kg ON kg.id_7 = rn.kontid
 LEFT JOIN vacpred vp ON vp.id_15 = rn.pred
 LEFT JOIN kontlist kl ON kl.op = rn.op
 LEFT JOIN kontkurs kk ON kk.id_1 = isnull(kl.kont, rn.kont)
 LEFT JOIN potoklist pl ON pl.op = rn.op
WHERE kk.fac = %(fac)s and rn.sem = %(sem)s
ORDER BY rn.id_51, op, grp, pred
        """

        nagr = Raspnagr.objects.raw(query % {
            "fac": BRIX_FACULTY_ID,
            "sem": self.get_semester(),
            "weeks_count": self.get_weeks_count(),
        })

        def process_nagr(items):
            items = list(items)
            first_item = items[0]
            return {
                "op": first_item.op,
                "discipline": first_item.pred,
                "teacher": first_item.prep,
                "hours": first_item.hours,
                "nt": first_item.nt,
                "groups_title": kont_obozn_process(first_item.grp),
                "kurs": first_item.kurs,
                'groups': [
                    {
                        "kont": kont_obozn_process(i.kont),
                        "kont_id": i.kont_id,
                        "kont_group": kont_obozn_process(i.kont_group),
                        "kont_group_id": i.kont_group_id,
                    } for i in items
                ],
                'groups_ids': [i.kont_id for i in items]
            }

        nagr = {
            _id: process_nagr(list(items))
            for _id, items in groupby(nagr, key=lambda x: x.id_51)
        }

        return Response(nagr)

    @action(detail=False)
    def set_nagruzka(self, request):
        RaspisZaoch.objects.create(

        )
