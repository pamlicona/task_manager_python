# Generated by Django 2.0.4 on 2018-06-10 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('initial_range', models.IntegerField()),
                ('final_range', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='final_duration',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='initial_duration',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='time_left',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='duration',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='task.Duration'),
            preserve_default=False,
        ),
    ]
