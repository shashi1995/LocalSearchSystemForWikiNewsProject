# Generated by Django 2.2.14 on 2020-08-05 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_wikinewsuser_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikinewsuser',
            name='is_admin',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]