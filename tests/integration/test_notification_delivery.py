import pytest
from django.contrib.auth.models import User
from voteapp.models import Incident, Notification

@pytest.mark.django_db
def test_notification_delivery():
    # Step 1: Create a reporter
    reporter = User.objects.create_user(username="reporter", password="securepassword")

    # Step 2: Create an incident with a reporter
    incident = Incident.objects.create(
        title="Voting System Outage",
        description="System downtime reported at precinct 7.",
        severity="Critical",
        status="Open",
        location="789 System Rd",
        reported_by=reporter  # Ensure this field matches your model
    )

    # Step 3: Create notifications
    notification1 = Notification.objects.create(
        incident=incident,
        message="IT team dispatched.",
        recipient="it_support@example.com"
    )
    notification2 = Notification.objects.create(
        incident=incident,
        message="Admin notified about system outage.",
        recipient="admin@example.com"
    )

    # Step 4: Verify notifications are tied to the incident
    notifications = Notification.objects.filter(incident=incident)
    assert notifications.count() == 2
    assert notification1 in notifications
    assert notification2 in notifications
