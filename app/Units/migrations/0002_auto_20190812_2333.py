# Generated by Django 2.2.4 on 2019-08-12 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Units', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='alternative_name',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
