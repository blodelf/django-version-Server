# Generated by Django 4.0.5 on 2022-06-05 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_restorepassword_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restorepassword',
            name='user',
            field=models.PositiveIntegerField(),
        ),
    ]
