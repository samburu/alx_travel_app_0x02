from django.db import models
import uuid


class User(models.Model):
    user_id = models.UUIDField(primary_key = True, default = uuid.uuid4, db_index=True)
    first_name = models.CharField(max_length=36)
    last_name = models.CharField(max_length=36)
    email = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=36)
    role = models.TextChoices('role', 'guest host admin')
    created_at = models.DateField()


class Listing(models.Model):
    listing_id = models.UUIDField(primary_key = True, default=uuid.uuid4, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=36)
    description = models.TextField()
    location = models.CharField(max_length=200)
    pricepernight = models.DecimalField(10,2)
    created_at = models.DateField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)

class Booking(models.Model):
    booking_id = models.UUIDField(primary_key = True, default=uuid.uuid4, db_index=True)
    property_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(10,2)
    status = models.TextChoices('status', 'pending confirmed canceled')
    created_at = models.DateField(auto_now_add=True)


class Review(models.Model):
    review_id = models.UUIDField(primary_key = True, default=uuid.uuid4, db_index=True)
    property_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerChoices(1,2,3,4,5)
    comment = models.TextField()
    created_at  = models.DateField(auto_now_add=True)


class Payment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]

    booking_reference = models.CharField(max_length=100, unique=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_reference} - {self.status}"