import pytest
from django.contrib.auth.models import User
from voteapp.models import Incident, Notification

@pytest.mark.django_db
def test_create_incident():
    # Create a user for testing
    user = User.objects.create_user(username="testuser", password="testpassword")
    
    # Test creating an emergency incident
    incident = Incident.objects.create(
        title="Power Outage at Voting Center",
        description="There is a power outage reported at the main voting center.",
        severity="High",
        status="Open",
        location="123 Voting Lane",
        reported_by=user  # Include reported_by
    )
    
    assert incident.title == "Power Outage at Voting Center"
    assert incident.description == "There is a power outage reported at the main voting center."
    assert incident.severity == "High"
    assert incident.status == "Open"
    assert incident.location == "123 Voting Lane"
    assert incident.reported_by == user

@pytest.mark.django_db
def test_update_incident_status():
    # Create a user for testing
    user = User.objects.create_user(username="testuser", password="testpassword")

    # Test updating the status of an incident
    incident = Incident.objects.create(
        title="Ballot Tampering Incident",
        description="Suspicious activity reported involving ballot tampering.",
        severity="Critical",
        status="Open",
        location="456 Election Ave",
        reported_by=user  # Include reported_by
    )
    
    incident.status = "Resolved"
    incident.save()

    updated_incident = Incident.objects.get(id=incident.id)
    assert updated_incident.status == "Resolved"

@pytest.mark.django_db
def test_incident_reporter_relationship():
    # Create a reporter (user)
    reporter = User.objects.create_user(username="reporter1", password="securepassword")
    
    # Test the relationship between an incident and its reporter
    incident = Incident.objects.create(
        title="Technical Glitch in Voting Machines",
        description="Voting machines malfunctioning in precinct 12.",
        severity="Medium",
        status="Open",
        location="789 Tech Rd",
        reported_by=reporter  # Use the correct field
    )
    
    assert incident.reported_by == reporter

@pytest.mark.django_db
def test_incident_notifications():
    # Create a user for testing
    user = User.objects.create_user(username="testuser", password="testpassword")
    
    # Test creating notifications for an incident
    incident = Incident.objects.create(
        title="Network Issue in Remote Voting",
        description="Network connectivity issue reported in remote voting setup.",
        severity="High",
        status="Open",
        location="321 Remote Center",
        reported_by=user  # Include reported_by
    )

    notification1 = Notification.objects.create(
        incident=incident,
        message="IT team dispatched to resolve the network issue.",
        recipient="it_support@ems.com"
    )

    notification2 = Notification.objects.create(
        incident=incident,
        message="Update: Network issue resolution in progress.",
        recipient="all_staff@ems.com"
    )

    assert incident.notifications.count() == 2
    assert notification1 in incident.notifications.all()
    assert notification2 in incident.notifications.all()

@pytest.mark.django_db
def test_severity_filter():
    # Create a user for testing
    user = User.objects.create_user(username="testuser", password="testpassword")

    # Test filtering incidents by severity level
    Incident.objects.create(
        title="Minor Delay in Ballot Delivery",
        description="Ballot delivery delayed due to traffic.",
        severity="Low",
        status="Open",
        location="123 Traffic St",
        reported_by=user  # Include reported_by
    )

    Incident.objects.create(
        title="Fire Drill at Voting Center",
        description="Unplanned fire drill causing disruption.",
        severity="High",
        status="Open",
        location="456 Safety Blvd",
        reported_by=user  # Include reported_by
    )

    high_severity_incidents = Incident.objects.filter(severity="High")
    assert high_severity_incidents.count() == 1
    assert high_severity_incidents.first().title == "Fire Drill at Voting Center"

@pytest.mark.django_db
def test_incident_resolver_relationship():
    # Create a resolver (user)
    resolver = User.objects.create_user(username="resolver1", password="securepassword")
    reporter = User.objects.create_user(username="reporter1", password="securepassword")

    # Test assigning a resolver to an incident
    incident = Incident.objects.create(
        title="Unauthorized Access Attempt",
        description="Attempt to access voting system by unauthorized personnel.",
        severity="Critical",
        status="Open",
        location="999 Security Ln",
        reported_by=reporter,  # Include reported_by
    )

    # Assign the resolver
    incident.resolver = resolver
    incident.save()

    assert incident.resolver == resolver
