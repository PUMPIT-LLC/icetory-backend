# Generated by Django 2.0.7 on 2018-08-17 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sberbank", "0003_auto_20180804_1932"),
    ]

    operations = [
        migrations.AddField(
            model_name="logentry",
            name="request_text",
            field=models.TextField(blank=True, null=True, verbose_name="request text"),
        ),
    ]
