from django.db import models
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User


class Incident(models.Model):
    INCIDENT_TYPES = [
        ('fire', 'Fire'),
        ('medical', 'Medical Emergency'),
        ('security', 'Security Threat'),
        ('disaster', 'Natural Disaster'),
    ]
    
    SEVERITY_LEVELS = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    incident_type = models.CharField(max_length=50, choices=INCIDENT_TYPES)
    urgency = models.CharField(max_length=50)  # E.g., 'Low', 'Medium', 'High'
    severity = models.CharField(max_length=50, choices=SEVERITY_LEVELS)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_incidents")
    resolver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="resolved_incidents")
    status = models.CharField(max_length=50, default="Pending")  # Pending, In Progress, Resolved
    reported_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reported_by.is_active:
            raise ValueError("User is inactive and cannot report an incident.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.incident_type}"


class Notification(models.Model):
    incident = models.ForeignKey(
        Incident, 
        on_delete=models.CASCADE, 
        related_name="notifications"
    )
    message = models.TextField()
    recipient = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.incident.title} to {self.recipient}"

class Candidate(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='candidates')
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote by {self.user.username} for {self.candidate.name}"





class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    total_vote = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, blank=True)
    
    def __str__(self):
        return self.title
    

class CategoryItem(models.Model):
    title = models.CharField(max_length=200)
    total_vote = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    voters = models.ManyToManyField(User, blank=True)
    
    @property
    def percentage_vote(self):
        category_votes = self.category.total_vote 
        item_votes = self.total_vote
        
        if category_votes == 0:
            vote_in_percentage = 0
        
        else:
            vote_in_percentage = (item_votes/category_votes) * 100
            
        return vote_in_percentage
    
    
    def __str__(self):
        return self.title