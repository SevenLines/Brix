from itertools import groupby

from django.views import View
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.schedule.consts import BRIX_FACULTY_ID
from apps.schedule.models import Raspnagr, RaspisZaoch
from apps.schedule.utils import kont_obozn_process


class BrixViewSet(ViewSet):
    @action(detail=False)
    def konts(self, request):
        query = """
        SELECT kk.id
        FROM raspnagr rn
         LEFT JOIN kontgrp kg ON kg.id_7 = rn.kontid
         LEFT JOIN kontlist kl ON kl.op = rn.op
         LEFT JOIN kontkurs kk ON kk.id_1 = isnull(kl.kont, rn.kont)
        WHERE kk.fac = %(fac)s and rn.sem = %(sem)s
        ORDER BY rn.id_51, op, grp, pred
                """

        nagr = Raspnagr.objects.raw(query % {
            "fac": BRIX_FACULTY_ID,
            "sem": 1,
            "weeks_count": 16,
        })

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
            "sem": 1,
            "weeks_count": 16,
        })

        def process_nagr(items):
            items = list(items)
            first_item = items[0]
            return {
                "op": first_item.op,
                "pred": first_item.pred,
                "teacher": first_item.prep,
                "hours": first_item.hours,
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

