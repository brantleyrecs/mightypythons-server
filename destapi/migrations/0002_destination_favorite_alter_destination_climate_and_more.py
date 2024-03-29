# Generated by Django 4.1.3 on 2024-02-07 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('destapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='favorite',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='destination',
            name='climate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='climate', to='destapi.climate'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='destapi.user'),
        ),
    ]
