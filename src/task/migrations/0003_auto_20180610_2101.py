# Generated by Django 2.0.4 on 2018-06-10 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20180610_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='final_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
