from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Transaction, AddBalance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        
class AddBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddBalance
        fields = '__all__'