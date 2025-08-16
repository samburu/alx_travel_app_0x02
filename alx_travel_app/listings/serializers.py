from rest_framework import serializers
from .models import User, Listing, Booking, Review

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['user_id', 'first_name', 'email']


class ListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Listing
		fields = ['owner', 'listing_id', 'name']


class BookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['booking_id', 'user_id', 'property_id', 'start_date', 'end_date']


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = ['review_id', 'property_id', 'rating']