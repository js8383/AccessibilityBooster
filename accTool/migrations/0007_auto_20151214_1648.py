# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 16:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accTool', '0006_auto_20151214_1643'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='parsed_image',
            new_name='ParsedImage',
        ),
    ]