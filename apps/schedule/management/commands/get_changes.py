import re
from itertools import groupby
from pprint import pprint

from django.core.management import BaseCommand
from django.db import connection

from apps.schedule.models import Raspnagr


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            query = cursor.execute("""
SELECT DISTINCT rtrim(coalesce(pl.konts, kg.obozn, kk.obozn)) as grp, vp.pred,
	r1.everyweek as everyweek1,
	r1.day as day1,
	r1.para as para1,
	isnull(al1.aud, r1.aud) as aud1,
	rn1.prep as prep1,
	r2.everyweek as everyweek2,
	r2.day as day2,
	r2.para as para2,
	isnull(al2.aud, r2.aud)  as  aud2,
	rn2.prep as prep2
FROM raspis r1
	LEFT JOIN raspnagr rn1 ON rn1.id_51 = r1.raspnagr
	LEFT JOIN kontkurs kk ON kk.id_1 = rn1.kont
	LEFT JOIN kontgrp kg ON kg.id_7 = rn1.kontid
	LEFT JOIN potoklist pl ON pl.op = rn1.op
	LEFT JOIN vacpred vp ON vp.id_15 = rn1.pred
	LEFT JOIN audlist al1 ON al1.auds = r1.aud
	LEFT JOIN SPR_POLITEX_CURRENT_SCHEDULE.dbo.raspis r2 ON r1.raspnagr = r2.raspnagr 
	LEFT JOIN SPR_POLITEX_CURRENT_SCHEDULE.dbo.raspnagr rn2 ON rn2.id_51 = r2.raspnagr
	--and (r1.num_zant - (SELECT min(num_zant) FROM raspis WHERE raspnagr = r1.raspnagr) = r2.num_zant - (SELECT min(num_zant) FROM SPR_POLITEX_CURRENT_SCHEDULE.dbo.raspis WHERE raspnagr = r1.raspnagr))
	LEFT JOIN SPR_POLITEX_CURRENT_SCHEDULE.dbo.audlist al2 ON al2.auds = r2.aud
WHERE (r2.everyweek is NULL or (r1.everyweek != r2.everyweek and r1.day != r2.day or r1.para != r2.para or r1.aud != r2.aud)) 
	and rn1.sem = 1
ORDER BY 1
            """)

            rows = list(query)
            data = {
                key: list(items)
                for key, items in groupby(rows, lambda x: "{}_{}".format(x.grp, x.pred))
            }

            groups = {}

            for key, items in data.items():
                old_items = sorted("{}_{}_{}_{}_{}".format(i.everyweek1, i.day1, i.para1, i.aud1, i.prep1) for i in items)
                new_items = sorted("{}_{}_{}_{}_{}".format(i.everyweek2, i.day2, i.para2, i.aud2, i.prep2) for i in items)

                old_items_auds = sorted("{}".format(i.aud1) for i in items)
                new_items_auds = sorted("{}".format(i.aud2) for i in items)

                old_items_preps = sorted("{}".format(i.prep1) for i in items)
                new_items_preps = sorted("{}".format(i.prep2) for i in items)

                old_items_schedule = sorted("{}_{}_{}".format(i.everyweek1, i.day1, i.para1) for i in items)
                new_items_schedule = sorted("{}_{}_{}".format(i.everyweek2, i.day2, i.para2) for i in items)

                if old_items != new_items:
                    item = groups.setdefault(key, {"group": "", "pred": "", "reasons": []})
                    item["group"] = items[0].grp
                    item["pred"] = items[0].pred
                    if 'None_None_None' in new_items_schedule:
                        item['reasons'].append("Добавление занятий")
                    elif old_items_schedule != new_items_schedule:
                        item['reasons'].append("Сдвиг занятий")
                    elif old_items_auds != new_items_auds:
                        item['reasons'].append("Смена аудитории")
                    elif old_items_preps != new_items_preps:
                        item['reasons'].append("Смена преподавателя")
                    else:
                        item['reasons'].append("Изменения в расписании")
                    # print(key, groups[key])

            groups_changed = set(group['group'] for group in groups.values())
            for group in sorted(groups_changed):
                print(group)

