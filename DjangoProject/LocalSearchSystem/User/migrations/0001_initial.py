# Generated by Django 3.0.7 on 2020-07-09 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=45)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('status', models.CharField(max_length=45)),
                ('usertype', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]