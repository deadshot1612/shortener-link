# Generated by Django 4.0.3 on 2022-03-26 13:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_userconfirmcode_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='userconfirmcode',
            name='sended',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
