# Generated by Django 5.1.2 on 2024-11-29 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0006_alter_transaction_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyairtime',
            name='request_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
