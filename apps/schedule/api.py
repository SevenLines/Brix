from itertools import groupby

from django.db.models.expressions import RawSQL
from django.views import View
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.schedule.consts import BRIX_FACULTY_ID
from apps.schedule.models import Raspnagr, RaspisZaoch, Kontkurs, Kontgrp, BrixModule, BrixRaspnagrToModules, Teacher
from apps.schedule.serializers import BrixSetNagruzkaSerializers, BrixModuleSerializer
from apps.schedule.utils import kont_obozn_process


class CommonViewSet(ViewSet):
    @action(detail=False)
    def teachers(self, request, *args, **kwargs):
        teachers = Teacher.objects.order_by("full_name")

        result = {
            i.id: {
                "id": i.id,
                "full_name": i.full_name.strip(),
                "short_name": i.short_name.strip(),
            } for i in teachers
        }

        return Response(result)


class BrixViewSet(ViewSet):
    def get_semester(self):
        return 1

    def get_weeks_count(self):
        return 16

    @action(detail=False)
    def konts(self, request, *args, **kwargs):
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

        query = list(query)

        grps = Kontgrp.objects.filter(kont__in=query).select_related('kont').order_by("kont")
        grps = {
            id_: list(items)
            for id_, items in groupby(grps, lambda x: x.kont.id)
        }

        result = {
            i.id: {
                'id': i.id,
                'title': kont_obozn_process(i.title),
                'groups': {
                    i.id: {
                        "id": i.id,
                        "kont": i.kont.id,
                        "title": kont_obozn_process(i.title),
                        "depth": i.depth,
                    }
                    for i in grps.get(i.id, [])}
            } for i in query
        }

        return Response(result)

    @action(detail=False, url_path="nagruzka")
    def nagruzka(self, request, *args, **kwargs):
        kont_id = request.query_params['kont_id']

        kont_condition = "TRUE"
        if kont_id:
            kont_condition = "coalesce(kl.kont, kg.kont, kk.id_1) = {}".format(kont_id)

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
    rn.prep as prep_id,
    rtrim(vp.pred) as pred,
    hy1 * %(weeks_count)s as hours
FROM raspnagr rn
 LEFT JOIN kontgrp kg ON kg.id_7 = rn.kontid
 LEFT JOIN vacpred vp ON vp.id_15 = rn.pred
 LEFT JOIN kontlist kl ON kl.op = rn.op
 LEFT JOIN kontkurs kk ON kk.id_1 = isnull(kl.kont, rn.kont)
 LEFT JOIN potoklist pl ON pl.op = rn.op
WHERE kk.fac = %(fac)s and rn.sem = %(sem)s AND %(kont_condition)s
ORDER BY rn.id_51, op, grp, pred
        """

        nagr = Raspnagr.objects.raw(query % {
            "fac": BRIX_FACULTY_ID,
            "sem": self.get_semester(),
            "kont_condition": kont_condition,
            "weeks_count": self.get_weeks_count(),
        })

        def process_nagr(items):
            items = list(items)
            first_item = items[0]
            return {
                "op": first_item.op,
                "discipline": first_item.pred,
                "teacher": first_item.prep_id,
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
                'groups_ids': [i.kont_id for i in items],
                'raspnagr_ids': [i.id for i in items]
            }

        nagr = {
            _id: process_nagr(list(items))
            for _id, items in groupby(nagr, key=lambda x: x.id)
        }

        return Response(nagr)

    @action(detail=False, methods=["POST"])
    def set_nagruzka(self, request, *args, **kwargs):
        serializer = BrixSetNagruzkaSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            rz = serializer.save()

        return Response({
            'raspis_id': rz.id
        })

    @action(detail=False, methods=["GET"])
    def raspis(self, *args, **kwargs):
        return Response({})


class BrixModulesViewSet(ViewSet):
    @action(detail=False, methods=["GET"], url_path="get-for-kont")
    def get_for_kont(self, request, *args, **kwargs):
        kont_id = request.query_params['kont_id']
        modules = BrixModule.objects.filter(konts__in=[kont_id])

        result = {}
        for m in modules:
            result[m.id] = {
                'date_start': m.date_start,
                'date_end': m.date_end,
                'title': m.title,
                'id': m.id,
            }

        return Response(result)

    @action(detail=False, methods=["GET"], url_path="get-hours-for-kont")
    def get_hours_by_raspnagr(self, request, *args, **kwargs):
        kont_id = request.query_params['kont_id']
        modules = BrixModule.objects.filter(konts__in=[kont_id])
        items = BrixRaspnagrToModules.objects.filter(module__in=modules)

        result = {}
        for i in items:
            raspnagr_item = result.setdefault(i.raspnagr_id, {})
            module_item = raspnagr_item.setdefault(i.module_id, {})
            module_item['hours'] = i.hours

        return Response(result)

    @action(detail=False, methods=['POST'], url_path="update-or-create")
    def update_or_create_kont(self, request, *args, **kwargs):
        serializer = BrixModuleSerializer(data=request.data)
        serializer.is_valid(True)

        data = {}
        if serializer.validated_data.get('id'):
            data['id'] = serializer.validated_data.get('id')

        module, _ = BrixModule.objects.update_or_create(**data, defaults={
            "kont_id": serializer.validated_data.get('kont_id'),
            "date_start": serializer.validated_data.get('date_start'),
            "date_end": serializer.validated_data.get('date_end'),
            "title": serializer.validated_data.get('title'),
        })

        return Response(BrixModuleSerializer(module).data)

    @action(detail=False, methods=["DELETE"], url_path="remove")
    def remove_module(self, request, *args, **kwargs):
        BrixModule.objects.filter(id=request.data.get('id')).delete()

        return Response({})
