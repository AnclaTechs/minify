# Generated by Django 2.2.6 on 2019-10-11 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0010_auto_20191010_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', tinymce.models.HTMLField(verbose_name='Content')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queanswers', to='base.Questions')),
            ],
            options={
                'verbose_name': 'Question-answer',
                'verbose_name_plural': 'Question-answer',
            },
        ),
        migrations.AlterModelOptions(
            name='quecomment',
            options={'verbose_name': 'Question-comment', 'verbose_name_plural': 'Question-comments'},
        ),
        migrations.AlterField(
            model_name='quecomment',
            name='body',
            field=models.TextField(max_length=300),
        ),
        migrations.CreateModel(
            name='QueAnswerComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=300)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queanswercomments', to='base.QueAnswer')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Question-answer Comment',
                'verbose_name_plural': 'Questions Comments',
            },
        ),
    ]
