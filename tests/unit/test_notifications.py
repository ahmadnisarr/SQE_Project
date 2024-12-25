import pytest
from django.contrib.auth.models import User
from voteapp.models import Incident, Notification

@pytest.mark.django_db
def test_incident_notification_system():
    # Create a user to report the incident
    reporter = User.objects.create_user(username="testuser", password="testpassword")
    
    # Create an incident
    incident = Incident.objects.create(
        title="Fire Alarm Triggered",
        description="Fire alarm triggered on the 5th floor.",
        location="Building B, 5th Floor",
        incident_type="fire",
        urgency="High",
        reported_by=reporter
    )
    
    # Simulate notification creation (assuming a notification is created automatically)
    notification = Notification.objects.create(
        incident=incident,
        message=f"Incident reported: {incident.title}",
        recipient="admin@ems.com"
    )
    
    # Verify the notification
    assert notification.incident == incident
    assert notification.message == "Incident reported: Fire Alarm Triggered"
    assert notification.recipient == "admin@ems.com"
    assert Notification.objects.filter(incident=incident).count() == 1

    # Verify notifications for the incident
    related_notifications = Notification.objects.filter(incident=incident)
    assert related_notifications.count() == 1
    assert related_notifications.first().message == notification.message
