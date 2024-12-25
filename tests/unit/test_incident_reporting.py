import pytest
from django.contrib.auth.models import User
from voteapp.models import Incident, Notification

@pytest.mark.django_db
def test_create_incident():
    # Create a user for testing
    user = User.objects.create_user(username="testuser", password="testpassword")
    
    # Create an incident
    incident = Incident.objects.create(
        title="Power Outage at Voting Center",
        description="There is a power outage reported at the main voting center.",
        severity="High",
        status="Open",
        location="123 Voting Lane",
        reported_by=user  # Associate with the user
    )
    
    assert incident.title == "Power Outage at Voting Center"
    assert incident.reported_by == user

    
@pytest.mark.django_db
def test_inactive_user_reporting_incident():
    # Create an inactive user
    user = User.objects.create_user(username="inactiveuser", password="testpassword", is_active=False)

    # Attempt to report an incident with an inactive user
    with pytest.raises(ValueError, match="User is inactive and cannot report an incident."):
        Incident.objects.create(
            title="Medical Emergency",
            description="A person has collapsed in the hallway.",
            location="Hallway",
            incident_type="medical",
            urgency="Medium",
            reported_by=user
        )

@pytest.mark.django_db
def test_incident_notification_on_report():
    # Create a user for testing
    user = User.objects.create_user(username="testuser", password="testpassword")

    # Report an incident
    incident = Incident.objects.create(
        title="Security Threat in Mall",
        description="Suspicious activity observed near the entrance.",
        location="Mall Entrance",
        incident_type="security",
        urgency="High",
        reported_by=user
    )

    # Create a notification manually for the incident
    notification = Notification.objects.create(
        incident=incident,
        message=f"New emergency incident reported: {incident.title}",
        recipient="admin@ems.com"
    )

    # Verify the notification is linked to the incident
    assert Notification.objects.filter(incident=incident).count() == 1
    assert notification.message == f"New emergency incident reported: {incident.title}"
    assert notification.recipient == "admin@ems.com"