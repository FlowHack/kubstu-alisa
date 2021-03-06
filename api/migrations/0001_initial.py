# Generated by Django 3.2.8 on 2021-10-13 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('user_id', models.CharField(max_length=70, unique=True, verbose_name='ID пользователя')),
                ('name', models.CharField(blank=True, default='Студент', max_length=15, verbose_name='Обращение')),
                ('faculties', models.CharField(blank=True, max_length=60, verbose_name='Название факультатива/института')),
                ('course', models.IntegerField(blank=True, verbose_name='Курс')),
                ('year_start_learn', models.IntegerField(blank=True, verbose_name='Год начала обучения')),
                ('form_of_learn', models.CharField(blank=True, max_length=2, verbose_name='Форма обучения')),
                ('direction', models.CharField(blank=True, max_length=3, verbose_name='Направление')),
                ('group', models.IntegerField(blank=True, verbose_name='Направление')),
                ('state', models.CharField(blank=True, default='Free', max_length=10, verbose_name='Состояние сессии')),
            ],
        ),
    ]
