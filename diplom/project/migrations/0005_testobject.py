# Generated by Django 3.0.4 on 2020-03-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20200309_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_field', models.CharField(max_length=100)),
            ],
        ),
    ]
