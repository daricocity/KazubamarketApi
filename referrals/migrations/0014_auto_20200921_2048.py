# Generated by Django 2.1 on 2020-09-21 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0013_referral_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='activated_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
