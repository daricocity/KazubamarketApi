# Generated by Django 2.1 on 2020-06-15 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0009_referral_has_paid_activation'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='activated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
