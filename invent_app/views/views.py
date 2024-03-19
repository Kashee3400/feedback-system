from django.shortcuts import render, get_object_or_404, redirect
from invent_app.forms import generate_dynamic_model_forms
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib import messages
from invent_app.tasks import send_email_after_delay,backup_database
from invent_app.models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.mail import EmailMessage
from invent import settings
from  webpush import send_user_notification
from celery.result import AsyncResult

@login_required
def index(request):
    # Check if the background task is already pending or executed
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")
    # result = send_email_after_delay.apply_async(args=[request.user.id])
    # db_result = backup_database.apply_async()
    return render(request, "invent_app/myadmin/dashboard.html")


@login_required
def profile(request):
    return render(request, "invent_app/myadmin/profile.html")

@login_required
def product_list(request):
    return render(request, "invent_app/myadmin/product-list.html")


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notification_test_page(request):
    current_user = request.user
    channel_layer = get_channel_layer()
    data = "notification" + "...." + str(datetime.now())
    user_id = str(current_user.pk)
    print(f'user-{user_id}')
    async_to_sync(channel_layer.group_send)(user_id,
        {
            "type": "notify",
            "text": data,
            'rejected_by': str(request.user)
        },
    )
    return render(request, 'invent_app/notify.html')


def notify(request):
    return render(request, 'index.html')


from django.urls import reverse

def notification(request):
    # Construct payload with URL
    notify_url = request.build_absolute_uri(reverse('user_profile'))
    notification_url = "https://kasheemilk.com"  # Replace this with the actual URL
    payload = {"head": "Low stock!", "body": "Stock is low. Please check ", "url": notify_url}
    
    # Send the notification
    send_user_notification(user=request.user, payload=payload, ttl=1000)
    
    webpush = {"group": 'inventory' }
    return render(request, 'invent_app/notification.html', {"webpush": webpush})