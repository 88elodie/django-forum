# Generated by Django 4.2.2 on 2023-07-12 20:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_alter_file_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(1, 'your title needs at least 1 character')]),
        ),
    ]
