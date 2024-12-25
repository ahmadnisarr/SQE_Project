# Generated by Django 4.2.5 on 2024-12-25 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voteapp', '0003_incident_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='resolver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_incidents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='incident',
            name='severity',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Critical', 'Critical')], default='low', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='incident',
            name='reported_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_incidents', to=settings.AUTH_USER_MODEL),
        ),
    ]