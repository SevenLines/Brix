from django.db import models


class Raspnagr(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_51")
    hy1 = models.IntegerField()
    nt = models.IntegerField()
    sem = models.IntegerField()
    kontid = models.ForeignKey("Kontgrp", db_column="kontid", on_delete=models.SET_NULL, null=True)
    prep = models.ForeignKey("Teacher", db_column="prep", on_delete=models.SET_NULL, null=True)

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


class AudSps(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_53")
    obozn = models.TextField(db_column="auds")
    stud = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'audsps'


class AudList(models.Model):
    auds = models.IntegerField()
    aud = models.ForeignKey("Auditory", db_column="aud", null=True, on_delete=models.SET_NULL)
    num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'audlist'


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
    full_name = models.TextField(db_column="prep")
    short_name = models.TextField(db_column="preps")

    class Meta:
        managed = False
        db_table = 'prepods'


class Kontgrp(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_7")
    title = models.TextField(db_column="obozn")
    kont = models.ForeignKey("Kontkurs", db_column="kont", on_delete=models.SET_NULL, null=True)
    students = models.IntegerField()
    parent = models.IntegerField()
    depth = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kontgrp'


class Kontkurs(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_1")
    fac = models.IntegerField()
    aobozn = models.IntegerField()
    kurs = models.IntegerField()
    groups = models.IntegerField()
    pgroups = models.IntegerField()
    stud = models.IntegerField()
    title = models.TextField(db_column="obozn", max_length=20)

    class Meta:
        managed = False
        db_table = 'kontkurs'


class RaspisZaoch(models.Model):
    raspnagr = models.ForeignKey("Raspnagr", db_column="raspnagr", on_delete=models.SET_NULL, null=True)
    aud = models.ForeignKey("Auditory", db_column="aud", on_delete=models.SET_NULL, null=True, related_name="+")
    aud2 = models.ForeignKey("Auditory", db_column="aud2", on_delete=models.SET_NULL, null=True, related_name="+")
    teacher = models.ForeignKey("Teacher", db_column="teacher", on_delete=models.SET_NULL, null=True)
    kont = models.ForeignKey("Kontkurs", db_column="kont", on_delete=models.SET_NULL, null=True)
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


class Raspis(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_55")
    raspnagr = models.ForeignKey("Raspnagr", db_column="raspnagr", on_delete=models.SET_NULL, null=True)
    everyweek = models.IntegerField()
    day = models.IntegerField()
    para = models.IntegerField()
    kol_par = models.IntegerField()
    # aud = models.ForeignKey("Auditory", db_column="aud", on_delete=models.SET_NULL, null=True)
    aud = models.IntegerField(db_column="aud", null=True)

    class Meta:
        managed = False
        db_table = 'raspis'


class Ownres(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_71")
    ownerid = models.IntegerField()
    obj = models.IntegerField()
    objid = models.ForeignKey("Kontkurs", db_column="objid", on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = False
        db_table = 'ownres'


class BrixModule(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    date_start = models.DateField()
    date_end = models.DateField()
    kont = models.ForeignKey("Kontkurs", null=True, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'brix_modules'


class BrixRaspnagrToModules(models.Model):
    id = models.AutoField(primary_key=True)
    raspnagr = models.ForeignKey("Raspnagr", null=True, on_delete=models.DO_NOTHING)
    module = models.ForeignKey("BrixModule", null=True, on_delete=models.DO_NOTHING)
    hours = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'brix_raspnagr_to_modules'