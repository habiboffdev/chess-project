# Generated by Django 5.0.7 on 2024-07-18 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chess', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['-match_date'], 'verbose_name_plural': 'Matches'},
        ),
    ]
