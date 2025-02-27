# Generated by Django 5.1.2 on 2025-02-14 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0022_tvservice_created_at_tvservice_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectricityBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceID', models.CharField(max_length=255)),
                ('meter_number', models.CharField(max_length=255)),
                ('meter_type', models.CharField(choices=[('Prepaid', 'Prepaid'), ('Postpaid', 'Postpaid')], max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
