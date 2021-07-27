# Generated by Django 3.2.5 on 2021-07-26 15:34

from django.db import migrations, models
import todos.models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0003_auto_20210723_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='avatars/default_profile_image.jpg', upload_to=todos.models.user_image_dir),
        ),
    ]
