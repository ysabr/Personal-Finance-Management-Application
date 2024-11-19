from rest_framework import serializers
from .models import Transaction

class Transactionerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'