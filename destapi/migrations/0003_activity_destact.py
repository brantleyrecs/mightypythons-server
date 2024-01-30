# Generated by Django 4.1.3 on 2024-01-30 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('destapi', '0002_destination'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('bio', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DestAct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dest_activities', to='destapi.activity')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='destapi.destination')),
            ],
        ),
    ]