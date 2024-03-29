# Generated by Django 3.1.5 on 2021-01-15 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_confirmed',
            field=models.BooleanField(default=False, verbose_name='确认状态'),
        ),
        migrations.CreateModel(
            name='ConfirmString',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256, verbose_name='确认码')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='确认时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='login.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '确认码',
                'verbose_name_plural': '确认码',
                'ordering': ['-c_time'],
            },
        ),
    ]
