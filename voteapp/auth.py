from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def authenticate_user(username, password):
    """
    Authenticates a user based on username and password.
    Returns a tuple of (user, message).
    """
    try:
        # Fetch the user object
        user = User.objects.get(username=username)
        if not user.is_active:
            # User exists but is inactive
            return None, "User account is inactive."
    except User.DoesNotExist:
        # User does not exist
        return None, "Invalid username or password."

    # Authenticate the user with the provided credentials
    user = authenticate(username=username, password=password)
    if user is None:
        # Authentication failed
        return None, "Invalid username or password."
    
    # Authentication successful
    return user, "Authentication successful."
