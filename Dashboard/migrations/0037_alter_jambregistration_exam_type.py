# Generated by Django 5.1.2 on 2025-04-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0036_alter_jambregistration_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jambregistration',
            name='exam_type',
            field=models.CharField(choices=[('Direct Entry (DE)', 'Direct Entry (DE)')], default='DE', max_length=20),
        ),
    ]
