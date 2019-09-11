from django.db import models


class Raspnagr(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_51")
    hy1 = models.IntegerField()
    nt = models.IntegerField()
    sem = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'raspnagr'

        # pred_id = db.Column("pred", db.Integer, db.ForeignKey("vacpred.id_15"))
    # kaf_id = db.Column("kaf", db.Integer, db.ForeignKey("vackaf.id_17"))
    # fobuch = db.Column(db.SmallInteger)
    # afobuch = db.Column(db.SmallInteger)
    # nagrid = db.Column(db.Integer)
    # h = db.Column(db.Float)
    # hy = db.Column(db.Integer)
    # dbeg = db.Column(db.Date)
    # days = db.Column(db.Integer)
    # prep_id = db.Column("prep", db.Integer, db.ForeignKey('prepods.id_61'))
    # aud_id = db.Column("aud", db.Integer, db.ForeignKey('auditories.id_60'))
    # nagrtype = db.Column(db.SmallInteger)
    # nagrprop = db.Column(db.Integer)
    # nagr_h = db.Column(db.Float)
    # stud = db.Column(db.Integer)
    # editstud = db.Column(db.Integer)
    # rnprep = db.Column(db.Integer)
    # # hy1 = db.Column(db.Integer)
    # # hy2 = db.Column(db.Integer)
    # syear = db.Column(db.Integer)


class Auditory(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_60")
    obozn = models.TextField()
    korp = models.IntegerField()
    maxstud = models.IntegerField()
    specoborud = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auditories'


class Teacher(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_61")
    full_name = models.TextField(name="prep")
    short_name = models.TextField(name="preps")

    class Meta:
        managed = False
        db_table = 'prepods'


class Kontkurs(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_7")
    title = models.TextField(db_column="obozn")
    kont = models.ForeignKey("Kontkurs", on_delete=models.SET_NULL, null=True)
    fac = models.IntegerField()
    aobozn = models.IntegerField()
    kurs = models.IntegerField()
    groups = models.IntegerField()
    stud = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kontgrp'


class Kontgrp(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_1")
    fac = models.IntegerField()
    aobozn = models.IntegerField()
    kurs = models.IntegerField()
    groups = models.IntegerField()
    stud = models.IntegerField()
    title = models.TextField(db_column="obozn")

class RaspisZaoch(models.Model):
    raspnagr = models.ForeignKey("Raspnagr", on_delete=models.SET_NULL, null=True)
    aud = models.ForeignKey("Auditory", on_delete=models.SET_NULL, null=True, related_name="+")
    aud2 = models.ForeignKey("Auditory", on_delete=models.SET_NULL, null=True, related_name="+")
    teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True)
    kont = models.ForeignKey("Kontkurs", on_delete=models.SET_NULL, null=True)
    kontgrp = models.IntegerField(null=True)
    type = models.IntegerField()
    op = models.IntegerField()
    dt = models.DateField()
    date_created = models.DateField(auto_now=True)
    para = models.IntegerField()
    hours = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'raspis_zaoch'
