# Generated by Django 3.2.2 on 2021-06-18 11:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20210618_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='last_login',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='msgread',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.CharField(default='offline', max_length=20),
        ),
        migrations.AddField(
            model_name='receiver',
            name='senderuser',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]