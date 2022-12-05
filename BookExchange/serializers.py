from rest_framework import serializers
from .models import Textbooks

class TextbooksSerializer(serializers.ModelSerializer):
	class Meta:
		model = Textbooks
		fields = ("name", "author", "condition", "creator", "price")
	
