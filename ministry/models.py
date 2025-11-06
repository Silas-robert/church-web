# models/database tables
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Sermon(models.Model):
    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='sermons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Sermon"
        verbose_name_plural = "Sermons"

    def __str__(self):
        return f"{self.title} - {self.preacher}"
    

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title} ({self.date})"
    @property
    def is_upcoming(self):
        return self.date >= timezone.now().date()

    @property
    def is_past(self):
        return self.date < timezone.now().date()
    

class Donation(models.Model):
    DONATION_TYPES = [
        ('Tithe', 'Tithe'),
        ('Offering', 'Offering'),
        ('Seed', 'Seed'),
        ('Other', 'Other'),
    ]

    PAYMENT_METHODS = [
        ('Mobile Money', 'Mobile Money'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash', 'Cash'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES, default='Offering')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS, default='Mobile Money')
    message = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.full_name} - {self.donation_type} ({self.amount})"
    

class Devotion(models.Model):
    CATEGORY_CHOICES = [
        ('article', 'Article'),
        ('devotional', 'Devotional'),
        ('teaching', 'Teaching'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='article')
    content = models.TextField()
    image = models.ImageField(upload_to='devotions/', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='devotions/pdfs/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title
    
class Testimony(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150, help_text="Short title for the testimony (e.g., 'Healed from sickness')")
    message = models.TextField(help_text="Full testimony message")
    image = models.ImageField(upload_to='testimonies/', blank=True, null=True)
    date_shared = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_shared']

    def __str__(self):
        return f"{self.name} - {self.title}"
    

class PrayerRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.message[:30]}"

    

class Gallery(models.Model):
    MEDIA_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default='image')
    media_file = models.FileField(upload_to='gallery/')
    event_date = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Membership(models.Model):
    INTEREST_CHOICES = [
        ('member', 'Becoming a Member'),
        ('volunteer', 'Volunteering for a Ministry'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    interest = models.CharField(max_length=20, choices=INTEREST_CHOICES)
    message = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_interest_display()}"

class Ministry(models.Model):
    CATEGORY_CHOICES = [
        ('Youth', 'Youth Ministry'),
        ('Women', 'Women Ministry'),
        ('Men', 'Men Ministry'),
        ('Children', 'Children Ministry'),
        ('Choir', 'Choir & Worship Team'),
        ('Project', 'Church Project'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='ministries/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class LiveStream(models.Model):
    title = models.CharField(max_length=255, default="Church Live Stream")
    url = models.URLField(help_text="Enter the embed link (e.g., YouTube embed URL)")
    is_active = models.BooleanField(default=False, help_text="Check if this stream is active")
    start_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
