# Generated by Django 3.2.2 on 2021-06-06 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='receiveType',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='message',
            name='recevier',
            field=models.CharField(default='', max_length=255),
        ),
    ]