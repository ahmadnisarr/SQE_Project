import pytest
from django.contrib.auth.models import User
from voteapp.auth import authenticate_user

@pytest.mark.django_db
def test_authenticate_user_valid_credentials():
    # Create a test user
    user = User.objects.create_user(username="testuser", password="testpassword")
    
    # Test valid credentials
    authenticated_user, message = authenticate_user(username="testuser", password="testpassword")
    assert authenticated_user == user
    assert message == "Authentication successful."


@pytest.mark.django_db
def test_authenticate_user_invalid_credentials():
    # Test invalid credentials
    authenticated_user, message = authenticate_user(username="invaliduser", password="wrongpassword")
    assert authenticated_user is None
    assert message == "Invalid username or password."


@pytest.mark.django_db
def test_authenticate_user_inactive_user():
    # Create an inactive user
    user = User.objects.create_user(username="inactiveuser", password="testpassword", is_active=False)
    
    # Test authentication of an inactive user
    authenticated_user, message = authenticate_user(username="inactiveuser", password="testpassword")
    assert authenticated_user is None
    assert message == "User account is inactive."
