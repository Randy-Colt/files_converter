from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Object(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Album(models.Model):
    class DocType(models.IntegerChoices):
        KJ = 1, 'КЖ'
        KM = 2, 'КМ'
        AR = 3, 'АР'

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    obj = models.ForeignKey(Object, on_delete=models.DO_NOTHING)
    name = models.TextField()
    doc_type = models.IntegerField(choices=DocType.choices)
    volume = models.FloatField(blank=True, null=True)
    filename = models.CharField(max_length=50)
    inventory_num = models.CharField(max_length=50)

    doc_mapping = {
        'КЖ': DocType.KJ,
        'КМ': DocType.KM,
        'АР': DocType.AR
    }
