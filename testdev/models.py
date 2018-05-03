# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TestCase(models.Model):
    #在django中会默认生成可以不用写这行
    #taskdesc, procallcount, amsid, metaruleid, production
    id = models.AutoField(primary_key=True)#用例编号
    taskdesc = models.CharField(max_length=50)
    procallcount = models.CharField(max_length=20)
    amsid = models.CharField(max_length=30)
    metaruleid = models.CharField(max_length=20)
    production = models.CharField(max_length=20)

    def __str__(self):
        return self.taskdesc
    class Meta():#设置缺省值
        #db_table = 'testcase'
        ordering=['id']
