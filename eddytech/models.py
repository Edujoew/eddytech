from django.db import models

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True) 
    description = models.TextField() 
    long_description = models.TextField(blank=True) 
    technologies = models.CharField(max_length=200, help_text="e.g. Django, React, PostgreSQL")
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"