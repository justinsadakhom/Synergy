# Generated by Django 3.0.2 on 2020-04-10 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synergy', '0006_auto_20200410_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='POSTAL_CODE',
            new_name='postal_code',
        ),
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(choices=[(None, '- Select -'), ('CAN', 'Canada'), ('OTH', 'Other')], max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='company_website',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
