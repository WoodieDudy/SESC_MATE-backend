# Generated by Django 3.1.1 on 2021-02-18 15:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0002_customannouncement'),
    ]

    operations = [
        migrations.AddField(
            model_name='customannouncement',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
