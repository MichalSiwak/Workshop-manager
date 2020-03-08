# Generated by Django 3.0.3 on 2020-02-26 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_mechanic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Numer stanowiska')),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_mechanic.Workshop')),
            ],
            options={
                'unique_together': {('number', 'workshop')},
            },
        ),
    ]
