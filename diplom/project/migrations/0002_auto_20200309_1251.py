# Generated by Django 2.2 on 2020-03-09 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recognizedobject',
            name='img_height',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='recognizedobject',
            name='img_width',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userphoto',
            name='img_height',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userphoto',
            name='img_width',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='recognizedobject',
            name='user_photo',
            field=models.ImageField(blank=True, height_field='img_height', null=True, upload_to='uploads/recognitation_faces', width_field='img_width'),
        ),
        migrations.AlterField(
            model_name='userphoto',
            name='user_photo',
            field=models.ImageField(height_field='img_height', upload_to='uploads', width_field='img_width'),
        ),
    ]
