# Generated by Django 2.2.6 on 2019-10-10 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_questions_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
