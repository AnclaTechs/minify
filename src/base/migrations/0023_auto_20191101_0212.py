# Generated by Django 2.2.6 on 2019-11-01 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20191028_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='notetype',
            field=models.CharField(choices=[('GEN', 'GENERAL NOTE/PROBLEM/SOLUTION'), ('HTSS', 'HTML/CSS'), ('PYTH', 'PYTHON'), ('JS', 'JAVASCRIPT'), ('C', 'C/C++'), ('PHP', 'PHP'), ('GO', 'GOLANG'), ('RUBY', 'RUBY'), ('JAVA', 'JAVA')], default='GEN', max_length=10),
        ),
    ]