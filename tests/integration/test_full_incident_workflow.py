import pytest
from django.contrib.auth.models import User
from voteapp.models import Incident, Notification

@pytest.mark.django_db
def test_full_incident_workflow():
    # Step 1: Create a reporter
    reporter = User.objects.create_user(username="reporter", password="securepassword")
    
    # Step 2: Create a resolver
    resolver = User.objects.create_user(username="resolver", password="securepassword")
    
    # Step 3: Report an incident
    incident = Incident.objects.create(
        title="Power Failure",
        description="Electricity outage at polling station.",
        severity="High",
        status="Open",
        location="123 Main St",
        reported_by=reporter
    )
    assert incident.reported_by == reporter

    # Step 4: Assign resolver and update status
    incident.resolver = resolver
    incident.status = "In Progress"
    incident.save()

    updated_incident = Incident.objects.get(id=incident.id)
    assert updated_incident.resolver == resolver
    assert updated_incident.status == "In Progress"

    # Step 5: Add notifications
    notification = Notification.objects.create(
        incident=incident,
        message="Maintenance team dispatched.",
        recipient="maintenance@example.com"
    )
    assert notification in Notification.objects.filter(incident=incident)
