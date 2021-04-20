# Generated by Django 3.1.1 on 2021-02-18 15:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0003_customannouncement_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customannouncement',
            name='order',
        ),
        migrations.AddField(
            model_name='customannouncement',
            name='is_pinned',
            field=models.BooleanField(default=False),
        ),
    ]