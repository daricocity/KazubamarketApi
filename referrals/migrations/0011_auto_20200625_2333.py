# Generated by Django 2.1 on 2020-06-25 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0010_referral_activated_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='path',
            field=models.TextField(),
        ),
    ]
