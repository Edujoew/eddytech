from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Project, Message, MpesaTransaction
from django_daraja.mpesa.core import MpesaClient

def index(request):
    return render(request, 'eddytech/index.html')

def work(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'eddytech/work.html', {'projects': projects})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        Message.objects.create(
            name=name, 
            email=email, 
            subject=subject, 
            message=message
        )

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
        return redirect('contact')

    return render(request, 'eddytech/contact.html')

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'eddytech/project_detail.html', {'project': project})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def support(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        
        try:
            amount_input = request.POST.get('amount')
            amount = int(float(amount_input))
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid positive amount.")
            return redirect('support')

        cl = MpesaClient()
        account_reference = 'EDYTECH_SUPPORT'
        transaction_desc = 'Support for John Edwards'
        callback_url = 'https://your-domain.com/mpesa/callback/' 

        try:
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            
            if response.response_code == '0':
                MpesaTransaction.objects.create(
                    checkout_request_id=response.checkout_request_id,
                    phone_number=phone_number,
                    amount=amount
                )
                return render(request, 'eddytech/waiting.html', {'checkout_id': response.checkout_request_id})
            else:
                messages.error(request, f"M-Pesa Error: {response.response_description}")
                return redirect('support')

        except Exception as e:
            messages.error(request, "Connection failed. Please check credentials.")
            return redirect('support')

    return render(request, 'eddytech/support.html')

def check_payment_status(request, checkout_id):
    transaction = get_object_or_404(MpesaTransaction, checkout_request_id=checkout_id)
    return JsonResponse({'status': transaction.status})

@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    result_code = data['Body']['stkCallback']['ResultCode']
    checkout_id = data['Body']['stkCallback']['CheckoutRequestID']
    
    transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_id)
    
    if result_code == 0:
        transaction.status = 'Success'
    else:
        transaction.status = 'Failed'
    
    transaction.save()
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})