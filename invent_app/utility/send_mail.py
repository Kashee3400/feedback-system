from invent import settings 
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from invent_app.models import CustomUser, Department
from django.urls import reverse
from datetime import datetime
from invent_app.models import Feedback, FarmerFeedback

def send_feedback_created_mail(request, feedback):
    subject = f'Feedback Received - #{feedback.feedback_id}'
    
    # Construct the email body using the provided feedback data

    message = (
        
        "We would like to acknowledge that we have received your feedback and it is valuable to us.\n"
        "A member of our team will review your feedback and take necessary actions accordingly.\n\n"
        "Thank you for taking the time to provide us with your input.\n"
    )
    context = {
        'name':f'{feedback.sender.first_name} {feedback.sender.last_name}',
        'message':message,
        'feedback_id':feedback.feedback_id
    }
    emp_email_html_message = render_to_string('email/feedback_email.txt', context)
    
    try:
        emp_email = EmailMessage(subject, emp_email_html_message, settings.EMAIL_HOST_USER, [feedback.sender.email])
        emp_email.send()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_feedback_status_mail(request, feedback):
    url = None
    reciever = None
    if isinstance(feedback, Feedback):
        reciever = feedback.receiver_feedback
        url = reverse('feedback_detail',args=[feedback.id])
    elif isinstance(feedback, FarmerFeedback):
        url = reverse('m_feedback_detail',args=[feedback.id])
        reciever = feedback.receiver_farmer

    subject = f'Your Feedback has been closed - #{feedback.feedback_id}'
    message = (
        "We Believe your (Issue) has been resolved as we did not receive any confirmation from your End, based on our last email communication, hence this case is ready to be closed as we have answered your queries regards to this ticket.\n\n"
        "Please feel free to get back to us if you feel the issue is not yet resolved or need more help on  this email,  contact us on  022 66628080\n\n"
        "Replying to the email not being one of them may lead to going this in history but not followed up. Hence request you to create a new ticket for every new issue you face.\n\n"
    )
    context = {
        'name':f'{feedback.sender.first_name} {feedback.sender.last_name}',
        'message':message,
        'feedback_id':feedback.feedback_id,
        'url':url
    }
    emp_email_html_message = render_to_string('email/feedback_email.txt', context)
    try:
        emp_email = EmailMessage(subject, emp_email_html_message, settings.EMAIL_HOST_USER, [feedback.sender.email],cc=[reciever.email])
        emp_email.send()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")


def send_member_feedback_created_mail(request, feedback):
    subject = f'Feedback Received - #{feedback.feedback_id}'
    # Construct the email body using the provided feedback data

    message = (
        
        "We would like to acknowledge that we have received your feedback and it is valuable to us.\n"
        "A member of our team will review your feedback and take necessary actions accordingly.\n\n"
        "Thank you for taking the time to provide us with your input.\n"
    )
    context = {
        'name':f'{feedback.first_name} ',
        'message':message,
        'feedback_id':feedback.feedback_id
    }
    emp_email_html_message = render_to_string('email/feedback_email.txt', context)
    
    try:
        emp_email = EmailMessage(subject, emp_email_html_message, settings.EMAIL_HOST_USER, [feedback.sender.email])
        emp_email.send()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_feedback_forwarded_mail(request, feedback):
    subject = f'Feedback Received - #{feedback.feedback_id}'
    # Construct the email body using the provided feedback data
    message = (
        f"You have new feedback from {feedback.sender.first_name} {feedback.sender.last_name}.\n"
    )
    url = None
    reciever = None
    if isinstance(feedback, Feedback):
        reciever = feedback.receiver_feedback
        url = reverse('feedback_detail',args=[feedback.id])
    elif isinstance(feedback, FarmerFeedback):
        url = reverse('m_feedback_detail',args=[feedback.id])
        reciever = feedback.receiver_farmer
        
    context = {
        'name':f'{reciever.first_name} {reciever.last_name}',
        'message':message,
        'feedback_id':feedback.feedback_id,
        'url':url
    }
    emp_email_html_message = render_to_string('email/feedback_email.txt', context)
    
    try:
        emp_email = EmailMessage(subject, emp_email_html_message, settings.EMAIL_HOST_USER, [reciever.email])
        emp_email.send()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")