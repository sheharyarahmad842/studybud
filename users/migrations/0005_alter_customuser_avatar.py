# Generated by Django 4.1.1 on 2022-11-26 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='https://res.cloudinary.com/dkcf3j3km/image/upload/v1669447116/avatar_txaab5.svg', upload_to='profile_pics'),
        ),
    ]
