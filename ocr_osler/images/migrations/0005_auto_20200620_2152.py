# Generated by Django 3.0.6 on 2020-06-20 21:52

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_auto_20200620_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='id',
        ),
        migrations.AddField(
            model_name='image',
            name='firmness',
            field=models.CharField(choices=[('unspecified', 'Unspecified'), ('soft', 'Soft'), ('semi-soft', 'Semi-Soft'), ('semi-hard', 'Semi-Hard'), ('hard', 'Hard')], default='unspecified', max_length=20, verbose_name='Firmness'),
        ),
        migrations.AlterField(
            model_name='image',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name', primary_key=True, serialize=False, unique=True, verbose_name='test slug'),
        ),
    ]
