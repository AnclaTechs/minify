# Generated by Django 2.2.6 on 2019-10-28 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_delete_pnotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
