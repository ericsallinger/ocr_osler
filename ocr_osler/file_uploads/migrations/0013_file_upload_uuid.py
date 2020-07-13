# Generated by Django 3.0.6 on 2020-07-10 18:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('file_uploads', '0012_auto_20200710_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='file_upload',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
    ]
