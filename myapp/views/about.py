from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def about_view(request):
    return render(request, "myapp/about.html")


def test_smtp_view(request):
    """
    Temporary view to test SMTP connectivity and log the results.
    """
    subject = "SMTP Connectivity Test from KidsPlayGround"
    message = "This is a test email sent from your Django application to check SMTP settings."
    # Use DEFAULT_FROM_EMAIL if set, otherwise fallback to EMAIL_HOST_USER.
    # If neither is set, this will be caught by the check below.
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    if not from_email:
        from_email = getattr(settings, 'EMAIL_HOST_USER', None)
    
    # Ensure there's a recipient. Sending to from_email itself for testing purposes.
    recipient_list = [from_email] if from_email else []

    if not from_email:
        log_message = "ERROR: DEFAULT_FROM_EMAIL or EMAIL_HOST_USER not configured for SMTP test."
        logger.error(log_message)
        return render(request, "myapp/about.html", {"test_result": log_message, "error": True})
    
    if not recipient_list:
        log_message = "ERROR: Recipient list is empty for SMTP test. DEFAULT_FROM_EMAIL or EMAIL_HOST_USER not configured."
        logger.error(log_message)
        return render(request, "myapp/about.html", {"test_result": log_message, "error": True})

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        log_message = f"SUCCESS: SMTP test email sent from {from_email} to {recipient_list[0]}."
        logger.info(log_message)
        return render(request, "myapp/about.html", {"test_result": log_message, "error": False})
    except Exception as e:
        log_message = f"ERROR: SMTP test email failed. Details: {e.__class__.__name__}: {e}"
        logger.error(log_message, exc_info=True)  # exc_info=True to log traceback
        return render(request, "myapp/about.html", {"test_result": log_message, "error": True})
