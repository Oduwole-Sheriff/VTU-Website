# Generated by Django 5.1.4 on 2024-12-29 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0016_remove_buydata_bypass_validator'),
    ]

    operations = [
        migrations.CreateModel(
            name='TVService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tv_service', models.CharField(choices=[('DSTV', 'DStv'), ('GOTV', 'GOtv'), ('STARTIMES', 'Startimes'), ('SHOWMAX', 'Showmax')], default='DSTV', max_length=10)),
                ('smartcard_number', models.CharField(blank=True, max_length=100, null=True)),
                ('iuc_number', models.CharField(blank=True, max_length=100, null=True)),
                ('action', models.CharField(blank=True, choices=[('renew', 'Renew Current Bouquet'), ('change', 'Change Bouquet')], max_length=100, null=True)),
                ('bouquet', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('startimes_smartcard', models.CharField(blank=True, max_length=100, null=True)),
                ('showmax_type', models.CharField(blank=True, choices=[('Movie', 'Movie'), ('Series', 'Series'), ('Documentary', 'Documentary')], max_length=50, null=True)),
            ],
        ),
    ]
