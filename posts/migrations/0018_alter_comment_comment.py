# Generated by Django 4.2.2 on 2023-07-16 15:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(max_length=300, validators=[django.core.validators.MinLengthValidator(1, 'your comment needs at least 1 character'), django.core.validators.MaxLengthValidator(300, 'your comment can only have 300 characters')]),
        ),
    ]
