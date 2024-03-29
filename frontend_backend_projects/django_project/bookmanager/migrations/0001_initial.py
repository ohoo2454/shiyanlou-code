# Generated by Django 3.1.5 on 2021-01-18 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='书名')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='价格')),
                ('pub_date', models.DateTimeField(default='2020-10-10 10:10:10', verbose_name='出版时间')),
                ('author', models.ManyToManyField(to='app01.Author', verbose_name='作者')),
                ('pub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.publisher', verbose_name='出版社')),
            ],
        ),
    ]
