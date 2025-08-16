from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
import requests
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# ---------------- Initiate Payment ----------------
@csrf_exempt
def initiate_payment(request):
    if request.method == "POST":
        try:
            data = request.POST
            booking_ref = data.get("booking_reference")
            amount = data.get("amount")
            email = data.get("email")

            # Unique transaction reference
            tx_ref = str(uuid.uuid4())

            headers = {
                "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
                "Content-Type": "application/json",
            }

            payload = {
                "amount": str(amount),
                "currency": "ETB",
                "email": email,
                "tx_ref": tx_ref,
                "callback_url": "http://localhost:8000/api/verify-payment/",
                "return_url": "http://localhost:8000/payment-success/",
            }

            response = requests.post(
                f"{settings.CHAPA_BASE_URL}/transaction/initialize",
                json=payload,
                headers=headers,
            )

            result = response.json()

            if result.get("status") == "success":
                Payment.objects.create(
                    booking_reference=booking_ref,
                    transaction_id=tx_ref,
                    amount=amount,
                    status="Pending",
                )
                return JsonResponse({"checkout_url": result["data"]["checkout_url"]})

            return JsonResponse(result, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# ---------------- Verify Payment ----------------
@csrf_exempt
def verify_payment(request):
    if request.method == "GET":
        tx_ref = request.GET.get("tx_ref")
        if not tx_ref:
            return JsonResponse({"error": "tx_ref required"}, status=400)

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        }

        response = requests.get(
            f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}",
            headers=headers,
        )

        result = response.json()
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)

            if result.get("status") == "success" and result["data"]["status"] == "success":
                payment.status = "Completed"
                payment.save()
                # Send confirmation email async via Celery
                from .tasks import send_payment_email
                send_payment_email.delay(payment.booking_reference, payment.amount)
            else:
                payment.status = "Failed"
                payment.save()

        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)

        return JsonResponse(result)
