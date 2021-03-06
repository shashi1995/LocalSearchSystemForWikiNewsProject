# Generated by Django 3.0.7 on 2020-07-13 18:46

import WikiNews.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WikiNews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemDetails',
            fields=[
                ('serialnumber', models.AutoField(primary_key=True, serialize=False)),
                ('article', WikiNews.models.BlobField(blank=True)),
                ('collaberation', WikiNews.models.BlobField(blank=True)),
                ('opinions', WikiNews.models.BlobField(blank=True)),
                ('sources', models.TextField(blank=True)),
                ('relatedarticles', models.TextField(blank=True)),
                ('externallinks', models.TextField(blank=True)),
                ('Item', models.ForeignKey(db_column='itemname', on_delete=django.db.models.deletion.CASCADE, to='WikiNews.Item')),
            ],
        ),
    ]
