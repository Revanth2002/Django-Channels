# Generated by Django 3.2.2 on 2021-06-18 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_alter_message_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='last_seen',
            field=models.CharField(default='2021-06-18 18:10:06.098537+05:30', max_length=255),
        ),
    ]