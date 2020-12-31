# Generated by Django 3.0.8 on 2020-08-25 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lend_and_returns', '0007_lendorder_total_received'),
    ]

    operations = [
        migrations.AddField(
            model_name='lendorder',
            name='amount_to_refund',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
