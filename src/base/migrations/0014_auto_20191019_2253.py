# Generated by Django 2.2.6 on 2019-10-19 21:53

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='users_vote',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
