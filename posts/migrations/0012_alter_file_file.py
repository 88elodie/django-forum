# Generated by Django 4.2.2 on 2023-07-05 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_rename_postfile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.CharField(max_length=100),
        ),
    ]
