# Generated by Django 2.2.6 on 2019-10-28 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_note'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PNotes',
        ),
    ]