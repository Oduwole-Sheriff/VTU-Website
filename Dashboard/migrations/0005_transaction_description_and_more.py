# Generated by Django 5.1.2 on 2024-11-28 21:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0004_alter_customuser_nin'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ('transfer', 'Transfer'), ('airtime_purchase', 'Airtime Purchase')], max_length=20),
        ),
        migrations.CreateModel(
            name='BuyAirtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.IntegerField(choices=[(1, 'MTN'), (2, 'GLO'), (3, '9MOBILE'), (4, 'AIRTEL')])),
                ('data_type', models.CharField(choices=[('VTU', 'VTU'), ('Share and Sell', 'Share and Sell')], max_length=20)),
                ('mobile_number', models.CharField(max_length=11)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bypass_validator', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='airtime_purchases', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]