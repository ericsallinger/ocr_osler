# Generated by Django 3.0.6 on 2020-06-20 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_uploads', '0002_auto_20200613_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='imageFile',
            field=models.ImageField(default='imagefiles/default.jpg', upload_to='imagefiles/'),
        ),
    ]