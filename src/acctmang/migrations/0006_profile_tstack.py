# Generated by Django 2.2.6 on 2019-11-03 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acctmang', '0005_profile_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tstack',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
