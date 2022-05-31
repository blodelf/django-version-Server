# Generated by Django 4.0.4 on 2022-05-25 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='dept_all',
            fields=[
                ('id', models.AutoField(db_column='dept_id', primary_key=True, serialize=False)),
                ('dept_ename', models.CharField(max_length=64, verbose_name='dept_ename')),
                ('dept_uname', models.CharField(max_length=64, verbose_name='dept_uname')),
                ('copymail', models.CharField(max_length=50, verbose_name='copymail')),
            ],
            options={
                'verbose_name': 'Dept all',
                'verbose_name_plural': 'Dept all',
            },
        ),
        migrations.CreateModel(
            name='faculty_all',
            fields=[
                ('id', models.AutoField(db_column='faculty_id', primary_key=True, serialize=False)),
                ('faculty', models.CharField(max_length=30, verbose_name='faculty')),
                ('dept_id', models.IntegerField(max_length=10, verbose_name='dept_id')),
            ],
            options={
                'verbose_name': 'Faculty All',
                'verbose_name_plural': 'Faculty All',
            },
        ),
        migrations.CreateModel(
            name='title_all',
            fields=[
                ('id', models.AutoField(db_column='title_id', primary_key=True, serialize=False)),
                ('title_uname', models.CharField(max_length=30, verbose_name='title_uname')),
                ('title_ename', models.CharField(max_length=30, verbose_name='title_ename')),
            ],
            options={
                'verbose_name': 'Title All',
                'verbose_name_plural': 'Title All',
            },
        ),
        migrations.CreateModel(
            name='users_access_group',
            fields=[
                ('id', models.AutoField(db_column='user_id', primary_key=True, serialize=False)),
                ('group_id', models.IntegerField(max_length=10, verbose_name='group_id')),
                ('desc', models.TextField(verbose_name='desc')),
            ],
            options={
                'verbose_name': 'users_access_group',
                'verbose_name_plural': 'users_access_group',
            },
        ),
        migrations.CreateModel(
            name='users_all',
            fields=[
                ('id', models.AutoField(db_column='user_id', primary_key=True, serialize=False)),
                ('dept_id', models.IntegerField(max_length=10, verbose_name='dept_id')),
                ('state', models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSED', 'CLOSED')], default='OPEN', max_length=10, verbose_name='state')),
                ('login', models.CharField(max_length=16, verbose_name='login')),
                ('passwd', models.CharField(max_length=40, verbose_name='passwd')),
                ('fname', models.CharField(max_length=50, verbose_name='fname')),
                ('lname', models.CharField(max_length=50, verbose_name='lname')),
                ('mname', models.CharField(max_length=50, verbose_name='mname')),
                ('contr_quest', models.CharField(max_length=255, verbose_name='contr_quest')),
                ('contr_answ', models.CharField(max_length=255, verbose_name='contr_answ')),
                ('title', models.CharField(max_length=30, verbose_name='title')),
                ('email', models.CharField(max_length=50, verbose_name='email')),
                ('phone', models.CharField(max_length=30, verbose_name='phone')),
                ('exp_date', models.DateTimeField(verbose_name='exp_date')),
                ('welcome_msg', models.CharField(max_length=255, verbose_name='welcome_msg')),
                ('admin', models.CharField(choices=[('n', 'n'), ('y', 'y')], default='n', max_length=2, verbose_name='admin')),
                ('document_id', models.CharField(max_length=16, verbose_name='document_id')),
                ('creator', models.CharField(max_length=16, verbose_name='creator')),
                ('operator', models.CharField(choices=[('n', 'n'), ('y', 'y')], default='n', max_length=2, verbose_name='operator')),
                ('mgroup_id', models.IntegerField(max_length=10, verbose_name='mgroup_id')),
                ('title_id', models.IntegerField(max_length=10, verbose_name='title_id')),
                ('admin_level', models.IntegerField(max_length=10, verbose_name='admin_level')),
            ],
            options={
                'verbose_name': 'users_all',
                'verbose_name_plural': 'users_all',
            },
        ),
        migrations.CreateModel(
            name='users_history',
            fields=[
                ('id', models.AutoField(db_column='user_id', primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('action', models.CharField(choices=[('CREATION', 'CREATION'), ('WARNING', 'WARNING'), ('CLOSING', 'CLOSING'), ('ACTIVATION', 'ACTIVATION'), ('CHPASS', 'CHPASS'), ('EXT_EXPIRE', 'EXT_EXPIRE'), ('CHDATA', 'CHDATA')], default='CREATION', max_length=20, verbose_name='Action')),
                ('creator', models.CharField(max_length=16, verbose_name='creator')),
                ('reason', models.TextField(verbose_name='reason')),
                ('ip', models.TextField(max_length=15, verbose_name='ip')),
            ],
            options={
                'verbose_name': 'users history',
                'verbose_name_plural': 'users history',
            },
        ),
    ]