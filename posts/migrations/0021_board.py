# Generated by Django 4.2.2 on 2023-07-19 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_alter_comment_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('members_only', models.BooleanField(default=False)),
            ],
        ),
    ]
