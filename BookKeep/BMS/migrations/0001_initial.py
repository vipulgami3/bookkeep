# Generated by Django 4.1 on 2022-10-27 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookKeep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('pages', models.IntegerField()),
                ('publication', models.CharField(max_length=100)),
                ('is_deleted', models.CharField(default='n', max_length=2)),
            ],
        ),
    ]
