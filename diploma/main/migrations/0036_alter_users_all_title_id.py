# Generated by Django 4.0.4 on 2022-05-29 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_alter_users_all_title_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users_all',
            name='title_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.title_all'),
        ),
    ]