# Generated by Django 4.2.5 on 2024-12-25 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voteapp', '0002_candidate_vote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('incident_type', models.CharField(choices=[('fire', 'Fire'), ('medical', 'Medical Emergency'), ('security', 'Security Threat'), ('disaster', 'Natural Disaster')], max_length=50)),
                ('urgency', models.CharField(max_length=50)),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('recipient', models.EmailField(max_length=254)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='voteapp.incident')),
            ],
        ),
    ]
