# Generated by Django 5.0.7 on 2024-07-19 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.BigIntegerField(default=1200),
        ),
    ]