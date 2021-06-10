# Generated by Django 2.2.20 on 2021-06-09 13:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=30)),
                ('slug', models.SlugField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Family',
                'verbose_name_plural': 'Families',
                'ordering': ('surname',),
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(blank=True, max_length=30)),
                ('patronymic', models.CharField(blank=True, max_length=30)),
                ('date_of_birth', models.DateField(blank=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=100)),
                ('date_of_death', models.DateField(blank=True)),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site.Family')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
                'ordering': ('surname',),
            },
        ),
        migrations.DeleteModel(
            name='BlogPost',
        ),
        migrations.AddField(
            model_name='family',
            name='id_husband',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_husband',
                                    to='site.Person'),
        ),
        migrations.AddField(
            model_name='family',
            name='id_wife',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_wife',
                                    to='site.Person'),
        ),
    ]
