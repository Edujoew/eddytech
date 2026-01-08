from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Project, Message

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to Database
        Message.objects.create(
            name=name, 
            email=email, 
            subject=subject, 
            message=message
        )

        # Send Email Notification
        email_subject = f"New Portfolio Message: {subject}"
        email_body = f"You received a new message from {name} ({email}):\n\n{message}"
        
        send_mail(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,  
            [settings.EMAIL_HOST_USER], 
            fail_silently=False,
        )

        messages.success(request, f"Thank you, {name}! Your message has been sent successfully.")
        return redirect('index')

    
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'eddytech/index.html', {'projects': projects})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'eddytech/project_detail.html', {'project': project})