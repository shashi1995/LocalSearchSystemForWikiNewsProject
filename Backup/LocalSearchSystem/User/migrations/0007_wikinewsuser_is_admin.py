# Generated by Django 3.0.8 on 2020-07-29 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_wikinewsuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikinewsuser',
            name='is_admin',
            field=models.BooleanField(default=True),
        ),
    ]
