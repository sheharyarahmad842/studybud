# Generated by Django 4.1.1 on 2023-02-07 13:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_id_alter_profile_temp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='temp_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
