from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_payment_email(booking_ref, amount):
    subject = "Booking Payment Confirmation"
    message = f"Your payment for booking {booking_ref} of amount {amount} ETB was successful."
    send_mail(subject, message, "noreply@alxtravel.com", ["user@example.com"])
