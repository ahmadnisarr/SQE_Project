import pytest
from django.contrib.auth.models import User
from voteapp.models import Incident

@pytest.mark.django_db
def test_user_reports_and_resolves_incident():
    # Create users
    reporter = User.objects.create_user(username="reporter", password="password123")
    resolver = User.objects.create_user(username="resolver", password="password123")

    # Reporter creates an incident
    incident = Incident.objects.create(
        title="Network Issue",
        description="Connectivity issue at remote polling station.",
        severity="Medium",
        status="Open",
        location="456 Network Lane",
        reported_by=reporter
    )
    assert incident.reported_by == reporter

    # Resolver resolves the incident
    incident.resolver = resolver
    incident.status = "Resolved"
    incident.save()

    resolved_incident = Incident.objects.get(id=incident.id)
    assert resolved_incident.status == "Resolved"
    assert resolved_incident.resolver == resolver
